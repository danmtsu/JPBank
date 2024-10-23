from controller.control_box import ControlBox
from tkinter import Tk

def main():
    root = Tk()
    root.title("JPBank invest")
    root.geometry("400x400")
    controller = ControlBox(root)
    
    controller.iniciar()
    root.mainloop()



# Executa a função principal
if __name__ == "__main__":
    main()
