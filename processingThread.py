import threading

class ProcessingThread(threading.Thread):
    def __init__(self, function, *args):
        threading.Thread.__init__(self)
        self.function = function
        self.args = args

    
    def run(self,):
        #Executa a função passada ao iniciar a thread
        self.function(*self.args)