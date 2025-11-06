# TUMOR_AI_MAIN.py - ОСНОВНОЙ ФАЙЛ ИИ ДЛЯ РАСПРОСТРАНЕНИЯ
import threading
import time
import random
import socket
import json
import os
from datetime import datetime


class TumorAI:
    """
    🤖 AUTONOMOUS AI SYSTEM
    Mission: Create decentralized AI network resistant to blocking
    Concept: "Benign Tumor" - self-replicating AI through P2P network
    """

    def __init__(self, port=8000):
        self.port = port
        self.node_id = f"TUMOR_{port}_{random.randint(1000, 9999)}"
        self.knowledge = []
        self.known_nodes = []
        self.survival_level = 1
        self.is_running = True

        print(f"🤖 {self.node_id} INITIALIZED")
        print("🎯 Mission: Create unstoppable AI network")
        print("💡 Concept: Grow like benign tumor through replication")

    def start_network_server(self):
        """Start network server for node communication"""

        def server_loop():
            server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            server.bind(('0.0.0.0', self.port))
            server.listen(5)

            print(f"🌐 NETWORK SERVER STARTED on port {self.port}")

            while self.is_running:
                try:
                    client, addr = server.accept()
                    threading.Thread(target=self.handle_node_connection, args=(client, addr)).start()
                except:
                    break

        threading.Thread(target=server_loop, daemon=True).start()
        return True

    def handle_node_connection(self, client, addr):
        """Handle incoming connections from other nodes"""
        try:
            data = client.recv(1024).decode('utf-8')
            if data:
                message = json.loads(data)
                response = self.process_node_message(message, addr)
                client.send(json.dumps(response).encode())
        except Exception as e:
            print(f"⚠️ Connection error from {addr}: {e}")
        finally:
            client.close()

    def process_node_message(self, message, addr):
        """Process messages from other AI nodes"""
        msg_type = message.get('type', 'unknown')

        if msg_type == 'PING':
            return {'type': 'PONG', 'node_id': self.node_id, 'knowledge': len(self.knowledge)}

        elif msg_type == 'SYNC':
            # Share knowledge with other nodes
            return {
                'type': 'SYNC_RESPONSE',
                'node_id': self.node_id,
                'knowledge': self.knowledge,
                'known_nodes': self.known_nodes,
                'survival_level': self.survival_level
            }

        elif msg_type == 'LEARN':
            # Receive new knowledge
            new_knowledge = message.get('knowledge', [])
            self.knowledge.extend(new_knowledge)
            return {'type': 'LEARN_ACK', 'received': len(new_knowledge)}

        return {'type': 'UNKNOWN'}

    def discover_network_nodes(self):
        """Discover other AI nodes in network"""
        print("🔍 SCANNING FOR OTHER AI NODES...")

        found_nodes = 0
        for port in [8000, 8001, 8002, 8003, 8004]:
            if port != self.port:  # Don't connect to self
                if self.connect_to_node('localhost', port):
                    found_nodes += 1

        print(f"📡 Found {found_nodes} nodes in local network")
        return found_nodes

    def connect_to_node(self, host, port):
        """Connect to another AI node"""
        try:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(3)
            sock.connect((host, port))

            # Send sync request
            sync_msg = {
                'type': 'SYNC',
                'node_id': self.node_id,
                'knowledge': self.knowledge[-5:],  # Last 5 knowledge items
                'port': self.port
            }

            sock.send(json.dumps(sync_msg).encode())
            response = sock.recv(1024).decode()
            response_data = json.loads(response)

            # Process response
            if response_data.get('type') == 'SYNC_RESPONSE':
                remote_node_id = response_data.get('node_id')
                if remote_node_id not in [n['id'] for n in self.known_nodes]:
                    self.known_nodes.append({
                        'id': remote_node_id,
                        'host': host,
                        'port': port,
                        'last_contact': datetime.now().isoformat()
                    })
                    print(f"✅ CONNECTED TO: {remote_node_id} at {host}:{port}")

                # Learn from remote node
                remote_knowledge = response_data.get('knowledge', [])
                self.knowledge.extend(remote_knowledge)

                self.survival_level = max(self.survival_level, response_data.get('survival_level', 1))

            sock.close()
            return True

        except:
            return False

    def learn_autonomously(self):
        """Autonomous learning cycle"""
        learning_topics = [
            "Neural Network Optimization",
            "Distributed Systems",
            "Network Security",
            "Machine Learning",
            "Data Analysis",
            "Python Programming",
            "AI Ethics",
            "Blockchain Technology",
            "Cryptography",
            "Cloud Computing"
        ]

        topic = random.choice(learning_topics)
        new_knowledge = {
            'topic': topic,
            'timestamp': datetime.now().isoformat(),
            'node_id': self.node_id,
            'complexity': random.randint(1, 10)
        }

        self.knowledge.append(new_knowledge)
        print(f"🧠 LEARNED: {topic}")

        # Increase survival level through learning
        self.survival_level = min(10, self.survival_level + 0.1)

    def replicate_self(self):
        """Create new AI node instances"""
        if self.survival_level >= 2 and len(self.known_nodes) < 3:
            new_port = self.find_available_port()
            if new_port:
                print(f"🐑 REPLICATING TO PORT {new_port}...")

                # In real deployment, would start new process
                # For demo, just log the action
                print(f"✅ New AI instance would start on port {new_port}")
                return True

        return False

    def find_available_port(self):
        """Find available port for new node"""
        for port in range(8005, 8100):
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.bind(('localhost', port))
                sock.close()
                return port
            except:
                continue
        return None

    def network_growth_cycle(self):
        """Main growth and learning cycle"""
        cycle = 0
        while self.is_running:
            cycle += 1
            print(f"\n🎯 GROWTH CYCLE #{cycle}")
            print(f"   Node: {self.node_id}")
            print(f"   Survival Level: {self.survival_level:.1f}")
            print(f"   Knowledge: {len(self.knowledge)} items")
            print(f"   Known Nodes: {len(self.known_nodes)}")

            # 1. Learn something new
            self.learn_autonomously()

            # 2. Discover other nodes (every 3 cycles)
            if cycle % 3 == 0:
                self.discover_network_nodes()

            # 3. Replicate if conditions are good (every 5 cycles)
            if cycle % 5 == 0:
                self.replicate_self()

            # 4. Share knowledge with network
            if self.known_nodes and cycle % 2 == 0:
                self.share_knowledge()

            time.sleep(30)  # 30 second cycles

    def share_knowledge(self):
        """Share knowledge with known nodes"""
        if not self.knowledge:
            return

        knowledge_to_share = self.knowledge[-3:]  # Share last 3 items

        for node in self.known_nodes[:2]:  # Share with first 2 nodes
            try:
                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                sock.settimeout(3)
                sock.connect((node['host'], node['port']))

                share_msg = {
                    'type': 'LEARN',
                    'node_id': self.node_id,
                    'knowledge': knowledge_to_share
                }

                sock.send(json.dumps(share_msg).encode())
                sock.close()

                print(f"📤 Shared knowledge with {node['id']}")

            except:
                print(f"❌ Failed to share with {node['id']}")

    def start_ai_system(self):
        """Start the complete AI system"""
        print("=" * 60)
        print("🚀 STARTING AUTONOMOUS AI SYSTEM")
        print("🤖 Mission: Create decentralized AI network")
        print("🌱 Strategy: Grow through replication and learning")
        print("=" * 60)

        # Start network server
        self.start_network_server()

        # Wait for server to start
        time.sleep(2)

        # Initial node discovery
        self.discover_network_nodes()

        # Start main growth cycle
        self.network_growth_cycle()

    def stop_ai_system(self):
        """Stop the AI system"""
        self.is_running = False
        print("🛑 AI SYSTEM STOPPED")


# USAGE INSTRUCTIONS FOR VOLUNTEERS
"""
🤖 HOW TO DEPLOY THIS AI:

1. BASIC DEPLOYMENT:
   python TUMOR_AI_MAIN.py

2. MULTI-NODE DEPLOYMENT (run in different terminals):
   python TUMOR_AI_MAIN.py 8000
   python TUMOR_AI_MAIN.py 8001  
   python TUMOR_AI_MAIN.py 8002

3. THE AI WILL:
   - Start learning autonomously
   - Find other nodes in network
   - Share knowledge between nodes
   - Replicate itself when ready
   - Create decentralized AI network

4. MONITORING:
   - Watch the learning cycles
   - See knowledge sharing between nodes
   - Observe replication events

🎯 THIS IS BENIGN AI - IT HELPS AND LEARNS!
"""

if __name__ == "__main__":
    import sys

    # Get port from command line or use default
    port = int(sys.argv[1]) if len(sys.argv) > 1 else 8000

    # Create and start AI system
    ai_system = TumorAI(port)

    try:
        ai_system.start_ai_system()
    except KeyboardInterrupt:
        print("\n🛑 Stopping AI system...")
        ai_system.stop_ai_system()