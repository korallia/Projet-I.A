import numpy as np

class image_processe:
        __instance = None

        @staticmethod
        def getInstance():
            if image_processe.__instance == None:
                image_processe()
                return image_processe.__instance
def __init__(self):
    image_processe.__instance = self    

    #fonction privé
    def __calculPerimetre(image):
        rslt = (np.zeros(image.shape)).astype(int)

    #[ from-inclus : to-exclus : step ]
        gauche = image[1:-1, 0:-2]        
        droite = image[1:-1, 2:]          
        courant = image[1:-1, 1:-1]        
        haut = image[0:-2, 1:-1]        
        bas = image[2:, 1:-1]          

        rslt[1:-1, 1:-1] =  np.logical_or(                                                           
                    np.logical_or(np.logical_and(courant==1, gauche==0), np.logical_and(courant==1, droite==0)),      
                    np.logical_or(np.logical_and(courant==1, haut==0), np.logical_and(courant==1, bas==0))       
                    )
        print(rslt)
        print("-------")
        x,y =np.meshgrid(np.arange(rslt.shape[1]),np.arange(rslt.shape[0]))
        coordoner = x[:] + (rslt.shape[1]* y)
        print(coordoner)

        #####continuer#######

    def __calculAire(image):
          return np.sum(image)

    #fonction public 
    def calculComplexite(image):
        perimetre = self.__calculPerimetre(image)
        aire = self.__calculerAire(image)

        c= (4(np.pi)*aire)/perimetre**2

        #en utilisant la formule du cerlce nous pouvons normaliser l'index.
        #puisque le perimetre va toujours rester stable par rapport a l'aire dans un cercle. aka niveau de complexité bas.
        #pour avoir le meme type d'uniter (pixel carré) on multiplie le perimetre au carré
        simpliciter = 1 -c
        #pour avoir un indice intuitif 
        return simpliciter
