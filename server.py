import socket
import threading
import random

HOST = '192.168.56.1'
PORT = 65432

clients = {}
team_odds = {team: round(random.uniform(2, 5), 2) for team in ["Team A", "Team B", "Team C", "Team D"]}

def handle_client(client_socket, addr):
    player_data = {'team': None, 'bet': 0, 'balance': 1000}
    client_socket.sendall("CONNECTED".encode())

    while True:
        try:
            data = client_socket.recv(1024).decode()
            if not data:
                break
            command, *args = data.split('|')

            if command == "JOIN":
                player_data['team'] = args[0]
                print(f"Player {addr} chose {player_data['team']}")

            elif command == "BET":
                player_data['bet'] = int(args[0])
                player_data['balance'] -= player_data['bet']

            elif command == "RESULT":
                winner = random.choice(list(team_odds.keys()))
                if player_data['team'] == winner:
                    winnings = player_data['bet'] * team_odds[winner]
                    player_data['balance'] += winnings
                client_socket.sendall(f"RESULT|{winner}|{player_data['balance']}".encode())
                
        except Exception as e:
            print(f"Error with client {addr}: {e}")
            break

    client_socket.close()
    del clients[addr]
    print(f"Player {addr} disconnected.")

def server_main():
    server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server.bind((HOST, PORT))
    server.listen(5)
    print("Server started... Waiting for players.")

    while True:
        client_socket, addr = server.accept()
        clients[addr] = client_socket
        print(f"Player {addr} connected.")
        threading.Thread(target=handle_client, args=(client_socket, addr)).start()

if __name__ == "__main__":
    server_main()
