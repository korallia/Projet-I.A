import numpy as np

from KNN import KNN

class image_processe:
        __instance = None


        @staticmethod
        def getInstance():
            if image_processe.__instance == None:
                image_processe()
                return image_processe.__instance
        def __init__(self, max_distance=1, nbr_voisins=3 ):
            image_processe.__instance = self    
            self.knn = KNN(max_distance, nbr_voisins )

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
            #print(rslt)
            #print("-------")
            return np.sum(rslt[rslt==1])
           # x,y =np.meshgrid(np.arange(rslt.shape[1]),np.arange(rslt.shape[0]))
           # coordoner = x[:] + (rslt.shape[1]* y)
#            print(coordoner)
 #           print("********")
  #          coordoner_perimetre = coordoner[rslt==1]
   #         print(coordoner_perimetre)
    #        divided = coordoner_perimetre[:]/coordoner.shape[1]
     #       modulo = coordoner_perimetre[:]%coordoner.shape[1]
      #      print(divided)
       #     print(modulo)
        #    print(coordoner.shape)
            #droite_perimetre = coordoner_perimetre[1:-1]
           # print(droite_perimetre)
            #perimetre = np.sum( ((coordoner_perimetre + droite_perimetre)**2))**0.5
           # perimetre = (np.sum( coordoner_perimetre)**2 + np.sum(droite_perimetre) **2)**0.5

            #print(perimetre)

        def __calculAire(self,image):
            return np.sum(image)

    #fonction public 
        def calculComplexite(self,image):
            perimetre = self.calculPerimetre(image)
            aire = self.__calculAire(image)

            c= (4*np.pi*aire)/perimetre**2

        #en utilisant la formule du cerlce nous pouvons normaliser l'index.
        #puisque le perimetre va toujours rester stable par rapport a l'aire dans un cercle. aka niveau de complexité bas.
        #pour avoir le meme type d'uniter (pixel carré) on multiplie le perimetre au carré
            simpliciter = 1 -c
        #pour avoir un indice intuitif 
            return simpliciter

        def indice2(self,image):
            return 1
        def indice3(self,image):
            return 0.5


        def __singleImageProcessing(self, arrayimage):
            if ( len(arrayimage) == 2 ):
                #print("########### FULL ARRAY IA #########")
                #print(arrayimage)
                #print("########### 0 #########")
                #print(arrayimage[0][0])
                tag = arrayimage[0][0]
                #print("########### 1 #########")
                #print(arrayimage[1][0])
                image  = arrayimage[1][0]
            else:
                image = arrayimage
                tag = ""
            indice1 = self.calculComplexite(image)
            indice2 = self.indice2(image)
            indice3 = self.indice3(image)


            if (tag != ""):
                return np.array([
                    indice1,
                    indice2,
                    indice3,
                    tag
                    ])
            else:
                return np.array([
                    indice1,
                    indice2,
                    indice3
                    ])


        def load_practice_images(self, images):
            func = np.vectorize(self.__singleImageProcessing,  signature='(m,n)->(o)')
            processed = func(images)
            self.knn.rajouter_image_a_espace_solution(processed)
            #print(processed)

        def process_unknown_image(self, image):
            processed = np.array( self.__singleImageProcessing(image))
            return self.knn.algo_knn(processed)
            





        



imgPro = image_processe.getInstance()
#imgPro.calculPerimetre(image)


image_a_calculer = np.array([
        [0,1,1,1,1,0],          # Gros rectangle
        [0,1,1,1,1,0], 
        [0,1,1,1,1,0], 
        [0,1,1,1,1,0], 
        [0,1,1,1,1,0], 
        [0,1,1,1,1,0],
        [0,1,1,1,1,0]   
    ])


nom_images = {
 0:"Gros Rectangle",
 1:"Petit Rectangle",
 2:"Gros H",
 3:"Moyen H",
 4:"Gros L",
 5:"Étoile"
}


images_a_calculer = np.array(        #différentes images de départ pour tests
    [
      [  [0],
        
            [np.array([
            [0,1,1,1,1,0],          # Gros rectangle
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0],
            [0,1,1,1,1,0]   
        ])]
      ]
    ,
     [[1],
        
       [ np.array([
        [0,0,0,0,0,0],        # Petit rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0],
        [0,0,0,0,0,0]   
        ])]]
    ,
     [[2],
        
     [np.array([
        [0,1,0,0,1,0],        # Gros H
        [0,1,0,0,1,0], 
        [0,1,0,0,1,0], 
        [0,1,1,1,1,0], 
        [0,1,0,0,1,0], 
        [0,1,0,0,1,0],
        [0,1,0,0,1,0]   
    ])]],
    
     [
         [3],
     [np.array([
         
         [0,0,0,0,0,0],        # Moyen H
         [0,1,0,1,0,0], 
         [0,1,0,1,0,0], 
         [0,1,1,1,0,0], 
         [0,1,0,1,0,0], 
         [0,1,0,1,0,0],
         [0,0,0,0,0,0]   
        ])]],
     [
         [4],
     [np.array([
        [0,1,1,0,0,0],        # Gros L
        [0,1,1,0,0,0], 
        [0,1,1,0,0,0], 
        [0,1,1,0,0,0], 
        [0,1,1,0,0,0], 
        [0,1,1,1,1,1],
        [0,1,1,1,1,1]   
        ])]],
     [
         [5],
     [np.array([
         [0,0,0,0,0,0],        # ~Étoile
         [1,0,0,0,0,0], 
         [0,1,0,0,0,0], 
         [0,0,1,1,1,1], 
         [0,0,1,0,0,0], 
         [0,0,0,1,1,0],
         [0,0,0,0,0,1]   
         ])]
      ]
    ])
      


imgPro.load_practice_images(images_a_calculer)
type = imgPro.process_unknown_image(image_a_calculer)
print(nom_images[type])
  