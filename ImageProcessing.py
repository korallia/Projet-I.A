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
        def calculPerimetre(self,image):
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
            print("********")
            coordoner_perimetre = coordoner[rslt==1]
            print(coordoner_perimetre)
            divided = coordoner_perimetre[:]/coordoner.shape[1]
            modulo = coordoner_perimetre[:]%coordoner.shape[1]
            print(divided)
            print(modulo)
            print(coordoner.shape)
            #droite_perimetre = coordoner_perimetre[1:-1]
           # print(droite_perimetre)
            #perimetre = np.sum( ((coordoner_perimetre + droite_perimetre)**2))**0.5
           # perimetre = (np.sum( coordoner_perimetre)**2 + np.sum(droite_perimetre) **2)**0.5

            #print(perimetre)

        def __calculAire(self,image):
            return np.sum(image)

    #fonction public 
        def calculComplexite(self,image):
            perimetre = self.__calculPerimetre(image)
            aire = self.__calculerAire(image)

            c= (4*np.pi*aire)/perimetre**2

        #en utilisant la formule du cerlce nous pouvons normaliser l'index.
        #puisque le perimetre va toujours rester stable par rapport a l'aire dans un cercle. aka niveau de complexité bas.
        #pour avoir le meme type d'uniter (pixel carré) on multiplie le perimetre au carré
            simpliciter = 1 -c
        #pour avoir un indice intuitif 
            return simpliciter

def draw_rectangle(image, top_left, bottom_right):
    top_left = (max(0,top_left[0]), max(0,top_left[1]))
    bottom_right = (min(image.shape[1],bottom_right[0]), min(image.shape[0],bottom_right[1]))
    image[top_left[1]:bottom_right[1],top_left[0]:bottom_right[0]] = 1
    print(image)

  



imgPro = image_processe.getInstance()
image =  np.zeros((8, 7), dtype=np.uint8)
draw_rectangle(image,(1,1),(5,4))
imgPro.calculPerimetre(image)



  