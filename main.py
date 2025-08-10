from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from kivy.uix.scrollview import ScrollView
from kivy.uix.gridlayout import GridLayout
from kivy.clock import Clock
import socket
import threading
import datetime
import json
from kivy.logger import Logger

class TCPServerApp(App):
    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # 服务器状态
        self.server_socket = None
        self.is_running = False
        self.clients = []
        self.teams = {}  # 存储队伍信息
        self.client_players = {}  # 存储客户端地址到角色名称的映射
        
    def build(self):
        # 主布局
        main_layout = BoxLayout(orientation='vertical', padding=10, spacing=10)
        
        # 标题
        title = Label(text='游戏组队自动化脚本服务器', size_hint_y=None, height=40, 
                     font_size=20, bold=True)
        main_layout.add_widget(title)
        
        # 服务器配置区域
        config_layout = BoxLayout(orientation='horizontal', size_hint_y=None, height=50)
        
        # IP地址输入
        config_layout.add_widget(Label(text='IP:', size_hint_x=None, width=50))
        self.ip_input = TextInput(text='0.0.0.0', size_hint_x=None, width=120, multiline=False)
        config_layout.add_widget(self.ip_input)
        
        # 端口输入
        config_layout.add_widget(Label(text='端口:', size_hint_x=None, width=50))
        self.port_input = TextInput(text='62333', size_hint_x=None, width=80, multiline=False)
        config_layout.add_widget(self.port_input)
        
        # 控制按钮
        self.start_btn = Button(text='启动服务器', size_hint_x=None, width=100)
        self.start_btn.bind(on_press=self.start_server)
        config_layout.add_widget(self.start_btn)
        
        self.stop_btn = Button(text='停止服务器', size_hint_x=None, width=100, disabled=True)
        self.stop_btn.bind(on_press=self.stop_server)
        config_layout.add_widget(self.stop_btn)
        
        main_layout.add_widget(config_layout)
        
        # 状态显示
        self.status_label = Label(text='服务器状态: 未启动', size_hint_y=None, height=30)
        main_layout.add_widget(self.status_label)
        
        # 队伍信息显示区域
        teams_label = Label(text='队伍信息:', size_hint_y=None, height=30, halign='left')
        main_layout.add_widget(teams_label)
        
        # 队伍信息滚动区域
        scroll = ScrollView(size_hint=(1, 0.3))
        self.teams_layout = GridLayout(cols=1, size_hint_y=None)
        self.teams_layout.bind(minimum_height=self.teams_layout.setter('height'))
        scroll.add_widget(self.teams_layout)
        main_layout.add_widget(scroll)
        
        # 日志显示区域
        log_label = Label(text='服务器日志:', size_hint_y=None, height=30, halign='left')
        main_layout.add_widget(log_label)
        
        # 日志滚动区域
        log_scroll = ScrollView()
        self.log_layout = GridLayout(cols=1, size_hint_y=None)
        self.log_layout.bind(minimum_height=self.log_layout.setter('height'))
        log_scroll.add_widget(self.log_layout)
        main_layout.add_widget(log_scroll)
        
        # 清除日志按钮
        clear_btn = Button(text='清除日志', size_hint_y=None, height=40)
        clear_btn.bind(on_press=self.clear_log)
        main_layout.add_widget(clear_btn)
        
        return main_layout
    
    def log_message(self, message):
        """添加日志消息"""
        timestamp = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        log_text = f"[{timestamp}] {message}"
        
        # 在主线程中更新UI
        Clock.schedule_once(lambda dt: self._add_log_to_ui(log_text), 0)
        Logger.info(f"TCP Server: {message}")
    
    def _add_log_to_ui(self, log_text):
        """在UI中添加日志"""
        log_label = Label(text=log_text, size_hint_y=None, height=30, 
                         text_size=(None, None), halign='left')
        self.log_layout.add_widget(log_label)
        
        # 限制日志数量，避免内存过多占用
        if len(self.log_layout.children) > 100:
            self.log_layout.remove_widget(self.log_layout.children[-1])
    
    def clear_log(self, instance):
        """清除日志"""
        self.log_layout.clear_widgets()
        self.log_message("日志已清除")
    
    def start_server(self, instance):
        """启动服务器"""
        if self.is_running:
            self.log_message("服务器已在运行中")
            return
        
        try:
            ip = self.ip_input.text.strip()
            port = int(self.port_input.text.strip())
            
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.server_socket.bind((ip, port))
            self.server_socket.listen(5)
            
            self.is_running = True
            self.log_message(f"服务器已启动，监听 {ip}:{port}")
            
            # 更新UI状态
            Clock.schedule_once(lambda dt: self._update_server_status(True), 0)
            
            # 启动接受连接的线程
            accept_thread = threading.Thread(target=self.accept_clients, daemon=True)
            accept_thread.start()
            
        except Exception as e:
            self.log_message(f"启动服务器失败: {str(e)}")
    
    def _update_server_status(self, running):
        """更新服务器状态UI"""
        if running:
            self.status_label.text = f'服务器状态: 运行中 ({self.ip_input.text}:{self.port_input.text})'
            self.start_btn.disabled = True
            self.stop_btn.disabled = False
        else:
            self.status_label.text = '服务器状态: 未启动'
            self.start_btn.disabled = False
            self.stop_btn.disabled = True
    
    def stop_server(self, instance):
        """停止服务器"""
        if not self.is_running:
            self.log_message("服务器未在运行")
            return
        
        try:
            self.is_running = False
            
            # 关闭所有客户端连接
            for client in self.clients[:]:
                try:
                    client.close()
                except:
                    pass
            self.clients.clear()
            
            # 关闭服务器socket
            if self.server_socket:
                self.server_socket.close()
                self.server_socket = None
            
            # 清空队伍数据
            self.teams.clear()
            self.client_players.clear()
            
            self.log_message("服务器已停止")
            
            # 更新UI状态
            Clock.schedule_once(lambda dt: self._update_server_status(False), 0)
            Clock.schedule_once(lambda dt: self.update_team_display(), 0)
            
        except Exception as e:
            self.log_message(f"停止服务器时出错: {str(e)}")
    
    def accept_clients(self):
        """接受客户端连接"""
        while self.is_running:
            try:
                if self.server_socket:
                    client_socket, client_addr = self.server_socket.accept()
                    self.clients.append(client_socket)
                    self.log_message(f"客户端连接: {client_addr}")
                    
                    # 为每个客户端创建处理线程
                    client_thread = threading.Thread(
                        target=self.handle_client, 
                        args=(client_socket, client_addr),
                        daemon=True
                    )
                    client_thread.start()
            except Exception as e:
                if self.is_running:
                    self.log_message(f"接受连接时出错: {str(e)}")
                break
    
    def handle_client(self, client_socket, client_addr):
        """处理客户端消息"""
        try:
            while self.is_running:
                data = client_socket.recv(1024)
                if not data:
                    break
                
                message = data.decode('utf-8').strip()
                self.log_message(f"收到来自 {client_addr} 的消息: {message}")
                
                # 处理JSON消息
                if self.is_valid_json(message):
                    response = self.process_json_message(message, client_addr)
                    if response:
                        response_str = json.dumps(response, ensure_ascii=False)
                        client_socket.send(response_str.encode('utf-8'))
                        self.log_message(f"向 {client_addr} 发送响应: {response_str}")
                else:
                    self.log_message(f"收到无效JSON消息: {message}")
                    
        except Exception as e:
            self.log_message(f"处理客户端 {client_addr} 时出错: {str(e)}")
        finally:
            self.handle_client_disconnect(client_addr)
            try:
                client_socket.close()
            except:
                pass
            if client_socket in self.clients:
                self.clients.remove(client_socket)
    
    def is_valid_json(self, message):
        """检查消息是否为有效JSON"""
        try:
            json.loads(message)
            return True
        except json.JSONDecodeError:
            return False
    
    def process_json_message(self, message, client_addr):
        """处理JSON消息并返回响应"""
        try:
            data = json.loads(message)
            info = data.get('info', '')
            
            if info == "创建队伍":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                scene_name = data.get('scene_name', '')
                status = data.get('status', 'true')
                team_count = data.get('team_count', '2')
                
                if team_id and player_name and scene_name:
                    self.create_team(team_id, player_name, scene_name, status, team_count)
                    self.client_players[client_addr] = player_name
                    self.log_message(f"玩家 {player_name} 创建了队伍 {team_id}，场景: {scene_name}")
                    Clock.schedule_once(lambda dt: self.update_team_display(), 0)
                    return {'message': 'ok'}
                else:
                    self.log_message(f"创建队伍失败：缺少必要参数")
                    return {'message': 'ok'}
            
            elif info == "加入队伍":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                status = data.get('status', 'true')
                
                if team_id and player_name:
                    success = self.join_team(team_id, player_name, status)
                    if success:
                        self.client_players[client_addr] = player_name
                        self.log_message(f"玩家 {player_name} 加入了队伍 {team_id}")
                        Clock.schedule_once(lambda dt: self.update_team_display(), 0)
                    else:
                        self.log_message(f"玩家 {player_name} 加入队伍 {team_id} 失败")
                    return {'message': 'ok'}
                else:
                    self.log_message(f"加入队伍失败：缺少必要参数")
                    return {'message': 'ok'}
            
            elif info == "申请入队":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                
                if team_id and player_name and team_id in self.teams:
                    team = self.teams[team_id]
                    leader_name = team['leader']
                    scene_name = team['scene']
                    
                    self.log_message(f"玩家 {player_name} 申请加入队伍 {team_id}")
                    return {
                        'leader_name': leader_name,
                        'scene_name': scene_name
                    }
                else:
                    self.log_message(f"申请入队失败：队伍 {team_id} 不存在或参数错误")
                    return {'message': 'false'}
            
            elif info == "离开队伍":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                
                if team_id and player_name:
                    self.leave_team(team_id, player_name)
                    self.log_message(f"玩家 {player_name} 离开了队伍 {team_id}")
                    Clock.schedule_once(lambda dt: self.update_team_display(), 0)
                    return {'message': 'ok'}
                else:
                    self.log_message(f"离开队伍失败：缺少必要参数")
                    return {'message': 'ok'}
            
            elif info == "更新状态":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                status = data.get('status', 'true')
                
                if team_id and player_name and team_id in self.teams:
                    team = self.teams[team_id]
                    if player_name == team['leader']:
                        team['leader_status'] = status
                        self.log_message(f"队长 {player_name} 更新状态为: {status}")
                    elif player_name in team['members']:
                        if 'member_status' not in team:
                            team['member_status'] = {}
                        team['member_status'][player_name] = status
                        self.log_message(f"队员 {player_name} 更新状态为: {status}")
                    Clock.schedule_once(lambda dt: self.update_team_display(), 0)
                    return {'message': 'ok'}
                else:
                    self.log_message(f"更新状态失败：队伍或玩家不存在")
                    return {'message': 'ok'}
            
            elif info == "查看队员":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                
                if team_id and player_name and team_id in self.teams:
                    team = self.teams[team_id]
                    if player_name == team['leader'] or player_name in team['members']:
                        team_count = int(team.get('team_count', '2'))
                        current_members = len(team['members']) + 1  # +1 for leader
                        
                        if current_members >= team_count:
                            leader_ready = team.get('leader_status', 'false') == 'true'
                            all_members_ready = True
                            
                            member_status = team.get('member_status', {})
                            for member in team['members']:
                                if member_status.get(member, 'false') != 'true':
                                    all_members_ready = False
                                    break
                            
                            if leader_ready and all_members_ready:
                                self.log_message(f"队伍 {team_id} 所有成员已准备就绪")
                                return {'message': 'true'}
                            else:
                                self.log_message(f"队伍 {team_id} 成员未全部准备就绪")
                                return {'message': 'false'}
                        else:
                            self.log_message(f"队伍 {team_id} 人数不足")
                            return {'message': 'false'}
                    else:
                        self.log_message(f"玩家 {player_name} 不在队伍 {team_id} 中")
                        return {'message': 'false'}
                else:
                    self.log_message(f"查看队员失败：队伍不存在或参数错误")
                    return {'message': 'false'}
            
            elif info == "更新场景":
                team_id = data.get('team_id', '')
                player_name = data.get('player_name', '')
                scene_name = data.get('scene_name', '')
                
                if team_id and player_name and scene_name and team_id in self.teams:
                    team = self.teams[team_id]
                    if player_name == team['leader']:
                        team['scene'] = scene_name
                        self.log_message(f"队长 {player_name} 更新场景为: {scene_name}")
                        Clock.schedule_once(lambda dt: self.update_team_display(), 0)
                        return {'message': 'ok'}
                return {'message': 'ok'}
            
            else:
                self.log_message(f"未知的消息类型: {info}")
                return {'message': 'ok'}
                
        except Exception as e:
            self.log_message(f"处理JSON消息时出错: {str(e)}")
            return {'message': 'ok'}
    
    def create_team(self, team_id, leader_name, scene_name, status='true', team_count='2'):
        """创建队伍"""
        self.teams[team_id] = {
            'leader': leader_name,
            'leader_status': status,
            'members': [],
            'member_status': {},
            'scene': scene_name,
            'team_count': team_count
        }
    
    def join_team(self, team_id, player_name, status='true'):
        """加入队伍"""
        if team_id not in self.teams:
            return False
        
        team = self.teams[team_id]
        team_count = int(team.get('team_count', '2'))
        current_members = len(team['members']) + 1  # +1 for leader
        
        if current_members >= team_count:
            return False
        
        if player_name not in team['members'] and player_name != team['leader']:
            team['members'].append(player_name)
            if 'member_status' not in team:
                team['member_status'] = {}
            team['member_status'][player_name] = status
            return True
        return False
    
    def leave_team(self, team_id, player_name):
        """离开队伍"""
        if team_id not in self.teams:
            return
        
        team = self.teams[team_id]
        if player_name == team['leader']:
            # 队长离开，解散队伍
            del self.teams[team_id]
        elif player_name in team['members']:
            # 队员离开
            team['members'].remove(player_name)
            if 'member_status' in team and player_name in team['member_status']:
                del team['member_status'][player_name]
    
    def update_team_display(self):
        """更新队伍显示"""
        self.teams_layout.clear_widgets()
        
        if not self.teams:
            no_teams_label = Label(text='暂无队伍', size_hint_y=None, height=30)
            self.teams_layout.add_widget(no_teams_label)
            return
        
        for team_id, team_info in self.teams.items():
            leader = team_info['leader']
            members = team_info.get('members', [])
            scene = team_info.get('scene', '未知')
            team_count = team_info.get('team_count', '2')
            leader_status = team_info.get('leader_status', 'false')
            member_status = team_info.get('member_status', {})
            
            # 队伍标题
            team_title = f"队伍ID: {team_id} | 场景: {scene} | 人数限制: {team_count}"
            title_label = Label(text=team_title, size_hint_y=None, height=30, bold=True)
            self.teams_layout.add_widget(title_label)
            
            # 队长信息
            leader_ready = "✓" if leader_status == 'true' else "✗"
            leader_text = f"  队长: {leader} {leader_ready}"
            leader_label = Label(text=leader_text, size_hint_y=None, height=25)
            self.teams_layout.add_widget(leader_label)
            
            # 队员信息
            if members:
                for member in members:
                    member_ready = "✓" if member_status.get(member, 'false') == 'true' else "✗"
                    member_text = f"  队员: {member} {member_ready}"
                    member_label = Label(text=member_text, size_hint_y=None, height=25)
                    self.teams_layout.add_widget(member_label)
            else:
                no_members_label = Label(text="  暂无队员", size_hint_y=None, height=25)
                self.teams_layout.add_widget(no_members_label)
            
            # 分隔线
            separator = Label(text="" + "-"*50, size_hint_y=None, height=20)
            self.teams_layout.add_widget(separator)
    
    def handle_client_disconnect(self, client_addr):
        """处理客户端断开连接"""
        if client_addr in self.client_players:
            player_name = self.client_players[client_addr]
            
            # 从所有队伍中移除该玩家
            teams_to_remove = []
            for team_id, team_info in self.teams.items():
                if player_name == team_info['leader']:
                    teams_to_remove.append(team_id)
                elif player_name in team_info.get('members', []):
                    team_info['members'].remove(player_name)
                    if 'member_status' in team_info and player_name in team_info['member_status']:
                        del team_info['member_status'][player_name]
            
            # 删除队长离开的队伍
            for team_id in teams_to_remove:
                del self.teams[team_id]
            
            del self.client_players[client_addr]
            self.log_message(f"玩家 {player_name} 断开连接")
            Clock.schedule_once(lambda dt: self.update_team_display(), 0)
    
    def on_stop(self):
        """应用关闭时的清理工作"""
        if self.is_running:
            self.stop_server(None)

if __name__ == '__main__':
    TCPServerApp().run()