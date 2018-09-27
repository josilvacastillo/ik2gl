#usr/bin/python3
# Script que genera los movimientos de un robot SCARA de 2 grados de libertad.
from tkinter import *
import math

BaseX  = 300      	#Punto X Base (hombro)  Situamos el brazo en pantalla.
BaseY  = 250      	#Punto Y Base (hombro)

LongBrazo  = 100  	# Longitud Brazo.        Puedes modificar las longitudes del brazo o antebrazo.     
LongAntBr  = 100  	# Longitud AnteBrazo.

x = 100           	# Posicion Inicial X.    Damos las get_coordinates iniciales de la mano del brazo.
y = 100      	# Posicion Inicial Y.    Se puede modificar los valores que están dentro del paréntesis.

class Cinematica_Inversa(Canvas):
	def __init__(self, root):
		root.title("Cinematica Inversa para Robot Scara")
		self.canvas = Canvas.__init__(self, root, width=BaseX*2, height=BaseY*2, bg='white')
		self.pack(expand=YES, fill=BOTH)
		self.create_data()
		self.rows = 20
		self.columns = 16
		self.draw_grid(self.rows,self.columns)
		self.print_axes()
		self.working_area()
		self.arms_init()
		


	def draw_grid(self, rows, columns):
		self.cellwidth = 25
		self.cellheight = 25
		rect = {}
		x0 = BaseX - self.cellwidth*rows/2
		y0 = BaseY - self.cellheight*columns/2

		for column in range(rows):
			for row in range(columns):
				x1 = x0 + column * self.cellwidth
				y1 = y0 + row * self.cellheight
				x2 = x1 + self.cellwidth
				y2 = y1 + self.cellheight
				rect[row, column] = self.create_rectangle(x1, y1, x2, y2)
		return x0, y0

	def working_area(self):
		area = self.create_oval(BaseX - (LongBrazo+LongAntBr), 
								BaseY - (LongBrazo+LongAntBr), 
								BaseX + (LongBrazo+LongAntBr), 
								BaseY + (LongBrazo+LongAntBr),
								outline='orange')

	def print_axes(self):
		x0, y0 = self.draw_grid(self.rows,self.columns)
		x_axe = self.create_line(x0 , BaseY, x0 + self.cellwidth*self.rows, BaseY, width=3)
		y_axe = self.create_line(BaseX, BaseY - self.cellheight*self.columns/2, BaseX, BaseY + self.cellheight*self.columns/2, width=3)

	def arms_init(self):
		BrazoPX, BrazoPY, AntBrazoPX, AntBrazoPY = self.get_coordinates() # Es otra manera de llamar a la funcion.
		self.brazo = self.create_line(BaseX, BaseY, BrazoPX, BrazoPY, fill='red', width=6)
		self.anteBrazo = self.create_line(BrazoPX, BrazoPY, AntBrazoPX, AntBrazoPY, fill='blue', width=4)
		self.mano = self.create_oval(AntBrazoPX-5, AntBrazoPY-5,AntBrazoPX+5, AntBrazoPY+5, fill='green')


	def get_coordinates(self):
		AngBrazo, AngAntBr = self.angle_calc()
		PYa = LongBrazo*-math.sin(AngBrazo)
		PYb = LongAntBr*-math.sin(AngAntBr+AngBrazo)
		PXa = LongBrazo*math.cos(AngBrazo)
		PXb = LongAntBr*math.cos(AngAntBr+AngBrazo)

		#BRAZO (x,y)
		BrazoPX = PXa+BaseX        # Punto de coordenada X del Brazo.
		BrazoPY = PYa+BaseY        # Punto de coordenada Y del Brazo.

		#ANTEBRAZO (x,y)
		AntBrazoPX = PXb+PXa+BaseX # Punto de coordenada X del AnteBrazo.
		AntBrazoPY = PYb+PYa+BaseY # Punto de coordenada Y del AnteBrazo.
		return BrazoPX, BrazoPY, AntBrazoPX, AntBrazoPY

	def arms_draw(self):
		BrazoPX, BrazoPY, AntBrazoPX, AntBrazoPY = self.get_coordinates()
		self.coords(self.brazo, BaseX, BaseY, BrazoPX, BrazoPY)
		self.coords(self.anteBrazo, BrazoPX, BrazoPY, AntBrazoPX, AntBrazoPY)
		self.coords(self.mano,AntBrazoPX-5, AntBrazoPY-5,AntBrazoPX+5, AntBrazoPY+5)

	def create_data(self):
		AngBrazo, AngAntBr = self.angle_calc()
		angulos = "Angulos  ---> Brazo:" + str(round(math.degrees(AngBrazo), 1)) + "º AnteBrazo:" + str(round(math.degrees(AngAntBr)+180,1)) + "º"
		get_coordinates = ("Coordenadas ---> " + str(x) + "X," + str(y) + "Y")

		self.widget_angle = Label(self, text=angulos, fg='black')
		self.widget_angle.pack()
		self.widget_get_coordinates = Label(self, text=get_coordinates, fg='black')
		self.widget_get_coordinates.pack()
		self.widget_direccion = Label(self, text='Usar las techas de direccion para mover el brazo.', fg='black')
		self.widget_direccion.pack()
		self.create_window(BaseX, 12, window=self.widget_angle)
		self.create_window(BaseX, 33, window=self.widget_get_coordinates)
		self.create_window(BaseX, 480, window=self.widget_direccion)

	def update_data(self):
		AngBrazo, AngAntBr = self.angle_calc()
		angulos = "Angulos  ---> Brazo:" + str(round(math.degrees(AngBrazo), 1)) + "º AnteBrazo:" + str(round(math.degrees(AngAntBr)+180,1)) + "º"
		get_coordinates = ("Coordenadas ---> " + str(x) + "X," + str(y) + "Y")
		self.widget_angle['text'] = angulos
		self.widget_get_coordinates['text'] = get_coordinates

	def angle_calc(self):
		LadoA = y
		Hipotenusa = math.sqrt((math.pow(LadoA,2)) + math.pow(x,2))
		Alfa = math.atan2(LadoA, x)
		Beta = math.acos( (math.pow(LongBrazo,2) - math.pow(LongAntBr,2) + math.pow(Hipotenusa,2) )/(2*LongBrazo*Hipotenusa) )
		AngBrazo = Alfa + Beta         # ANGULO BRAZO(en radianes).

		Gamma = math.acos((math.pow(LongBrazo,2) + math.pow(LongAntBr,2) - math.pow(Hipotenusa,2) )/(2*LongBrazo*LongAntBr) )
		AngAntBr = Gamma - math.radians(180)    # ANGULO ANTEBRAZO(en radianes).
		return AngBrazo, AngAntBr

	def edge_condition(self, _x, _y):
		maximo = math.sqrt(math.pow(_x,2) + math.pow(_y,2))
		if maximo <= (LongAntBr+LongBrazo):
			return True
		else: 
			return False

	def keypress(event):
		global x, y
		if event.keysym == 'Up': y = y + 1
		if event.keysym == 'Down': y = y - 1
		if event.keysym == 'Left': x = x - 1
		if event.keysym == 'Right': x = x + 1
		
		if not frame.edge_condition(x, y) or x == 0 and y == 0:
			if event.keysym == 'Up': y = y - 1
			if event.keysym == 'Down': y = y + 1
			if event.keysym == 'Left': x = x + 1
			if event.keysym == 'Right': x = x - 1
		frame.arms_draw()
		frame.update_data()


root = Tk()
frame = Cinematica_Inversa(root)
root.bind("<Key>", Cinematica_Inversa.keypress)
root.mainloop()



