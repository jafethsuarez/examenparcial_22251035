import socket
import threading
import sys
import pickle
import os
import re as reg


class Servidor():  # se hace una clase para llamarla como el main en c

	# saber el puerto e ip del host
	def __init__(self, host=socket.gethostname(), port=int(input("Que puerto quiere usar ? "))):
		self.clientes = []
		self.nicknames = []
		print('\nSu IP actual es : ', socket.gethostbyname(host))
		print('\n\tProceso con PID = ', os.getpid(), '\n\tHilo PRINCIPAL con ID =', threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ',
		      threading.currentThread().isDaemon(), '\n\tTotal Hilos activos en este punto del programa =', threading.active_count())
		self.s = socket.socket()
		self.s.bind((str(host), int(port)))  # enlazar el host y el puerto
		self.s.listen(30)  # espera a que conexiones entren
		self.s.setblocking(False)

		# evitar race condition
		threading.Thread(target=self.aceptarC, daemon=True).start()
		threading.Thread(target=self.procesarC, daemon=True).start()

		while True:
			Array_Dim=[1035,22,1035]
			msg = input('\n << SALIR = 1 >> \n')
			if msg == '1':
				print(" **** Me piro vampiro; cierro socket y mato SERVER con PID = ", os.getpid())
				self.s.close()
				sys.exit()
#			else: pass
			else:
				for c in self.clientes:
					c.send(pickle.dumps(Array_Dim))
              
	def aceptarC(self):
		print('\nHilo ACEPTAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())
		while True:
			try:
				conn, addr = self.s.accept()
				print(f"\nConexion aceptada via {addr}\n")
				conn.setblocking(False)
				self.clientes.append(conn)
			except: pass

	def procesarC(self):
		print('\nHilo PROCESAR con ID =',threading.currentThread().getName(), '\n\tHilo en modo DAEMON = ', threading.currentThread().isDaemon(),'\n\tPertenece al PROCESO con PID', os.getpid(), "\n\tHilos activos TOTALES ", threading.active_count())  
		while True:
			if len(self.clientes) > 0:   ##si no hay clientes conectados no se procesa
				for c in self.clientes:
					try:
						data = c.recv(64)                   ##espero y si hay alguien hago el broadcast
						if data: self.broadcast(data,c)
					except: pass

	def broadcast(self, msg, cliente):        ##enviar el mensaje a todos
		str=pickle.loads(msg)
		found=reg.search('^[^ :]*',str)
		if found.group() not in self.nicknames:
			self.nicknames.append(found.group())
		with open("u22045519AI1.txt", "a") as f:
			f.write("\n" + str)
			f.close()
		for c in self.clientes:               ## decir cuantos clientes hay conectados
			print("Clientes conectados Right now = ", len(self.clientes))
			print("LISTA DE CLIENTES (NICKNAMES)")
			for n in self.nicknames:
				print(n)
			try:
				if c != cliente:              ## si cliente != array cliente cargo el mensaje y lo envio a todos
					print(pickle.loads(msg))
					c.send(msg)
			except: self.clientes.remove(c)   ## si falla entonces no hay clientes y lo quito

arrancar = Servidor() 