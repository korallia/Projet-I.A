import array
import numpy as np

from KNN import KNN

class image_processe:
        def __init__(self):
            self.__nbr_index = 3
            self.__private = True

    #fonction privé
        def __calculPerimetre(self,image):
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
            
            """ méthode 2 périmetre non compléter
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
            droite_perimetre = coordoner_perimetre[1:-1]
            print(droite_perimetre)
            perimetre = np.sum( ((coordoner_perimetre + droite_perimetre)**2))**0.5
             perimetre = (np.sum( coordoner_perimetre)**2 + np.sum(droite_perimetre) **2)**0.5

            print(perimetre)
            """

            return np.sum(rslt[rslt==1])
            

           
        def __calculAire(self,image):
            return np.sum(image)

        def __centroidYX(self, image):
            aire = self.__calculAire(image)
            c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
            return (np.sum(r * image), np.sum(c * image)) / aire
        
        def __distance_centroide(self, image):
            centroide= self.__centroidYX(image)

        # Créer un meshgrid avec dimensions de notre image
            c, r = np.meshgrid(np.arange(image.shape[1]), np.arange(image.shape[0]))
            print("image.shape[0]: ", image.shape[0], 
                "\timage.shape[1]: ", image.shape[1], 
                "\timage.shape: ", image.shape)

        # Sortir les coord des 1 de l'image avec les 2 matrices retournees par le meshgrid
        # print("\nles X des cases avec des 1:\n", c[image>0])
        # print("les Y des cases avec des 1:\n", r[image>0])

        # Créer une matrice unidimensionnelle pour stocker les calculs de distance
            calcul = np.zeros((c[image>0].shape[0]))
            calcul[:] = (   (c[image>0] - centroide[1])**2 + 
                        (r[image>0] - centroide[0])**2      )**0.5    
            return calcul
        # Avec la matrice de distances, on fait np.std(calcul) et ça donne l'écart-type (O)
        # On peut, je crois, "normaliser" l'écart-type (O), avec le range, en faisant : 
        # 2 x écart-type / range, donc  : 2*(O) / (max-min), 
        # car le range est toujours plus grand que 6 * écart-types pour 99.9...%, 
        # donc on aura un quotient plus petit que 1...

        def __calculComplexite(self,image):
            perimetre = self.__calculPerimetre(image)
            aire = self.__calculAire(image)

            c= (4*np.pi*aire)/perimetre**2
            simpliciter = 1 -c
            return abs(simpliciter)

        def __rayon_i_sur_c(self,image):
            data_distance = self.__distance_centroide(image)
            min =  np.min(data_distance)
            max = np.max(data_distance)
            return   min/max
        def __aire_sur_aire_c(self,image):
            data_aire = self.__calculAire(image)
            data_distance = self.__distance_centroide(image)
            max = np.max(data_distance)
            aire_circonscrit = np.pi*max**2       
            return data_aire / aire_circonscrit 

        def __singleImageProcessing(self, arrayimage):
            if ( len(arrayimage) == 2 ):
                tag = arrayimage[0][0]
                image  = arrayimage[1][0]
            else:
                image = arrayimage
                tag = ""
            indice1 = self.__calculComplexite(image)
            indice2 = self.__rayon_i_sur_c(image)
            indice3 = self.__aire_sur_aire_c(image)


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

        @property
        def nbr_metrics(self):
            return self.__nbr_metrics
        @property.setter
        def nbr_metrics(self,value):
            self.__nbr_metrics = value

        
        def load_practice_images(self, images,taglist,knn):
            stack = np.zeros((0,2))
            for key, _ in enumerate(images):
                stack = np.append( stack, [(np.array([ taglist[key], images[key] ]))], axis=0)
            
            func = np.vectorize(self.__singleImageProcessing,  signature='(m,n)->(o)')
            processed = func(stack)
            knn.rajouter_image_a_espace_solution(processed)
           

        def process_unknown_image(self, image,knn):
            processed = np.array( self.__singleImageProcessing(image))
            return knn.algo_knn(processed)
            



image_a_calculer = np.array([
        [0,0,0,0,0,0],          # Gros rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]   
    ])
image1 = np.array([
        [0,0,0,0,0,0],          # Gros rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,0,0,0,0,0],
        [0,0,0,0,0,0]   
    ])
image2 = np.array([
        [0,0,0,0,0,0],        # Petit rectangle
        [0,0,0,0,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0], 
        [0,1,1,1,0,0],
        [0,0,0,0,0,0]   
        ])

image_list = [
[image1],
[image2],
[image2]
]


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
            [0,0,0,0,0,0],          # Gros rectangle
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0], 
            [0,1,1,1,1,0],
            [0,0,0,0,0,0]   
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
        [0,0,0,0,0,0],        # Gros H
        [0,1,0,0,1,0], 
        [0,1,0,0,1,0], 
        [0,1,1,1,1,0], 
        [0,1,0,0,1,0], 
        [0,1,0,0,1,0],
        [0,0,0,0,0,0]   
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
        [0,0,0,0,0,0],        # Gros L
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
         [0,0,0,0,0,0], 
         [0,1,0,0,0,0], 
         [0,0,1,1,1,1], 
         [0,0,1,0,0,0], 
         [0,0,0,1,1,0],
         [0,0,0,0,0,0]   
         ])]
      ]
    ])
      

imgpro = image_processe()
#imgpro.load_practice_images(images_a_calculer)
#type = imgPro.process_unknown_image(image_a_calculer)
#
# print(nom_images[type])
#print(images_a_calculer[:,0])
#array = np.zeros((2,2,1))
print("-----------")
id_list = [1,2,3]
#array[:,0,0] = id_list
#array[:,1,0] = image_list



tag_list = np.array(id_list)
print ( tag_list)
tag_list = np.reshape(tag_list, ( len(tag_list), 1 ))
print ( tag_list)
print("------------")
print ( image_list)
images_np = np.array(image_list)
print ( images_np)


stack = np.zeros((0,2))
for key, _ in enumerate(image_list):
    stack = np.append( stack, [(np.array([ id_list[key], image_list[key] ]))], axis=0)
print( "------------------")
print( stack)


#stack = np.vstack((tag_list, images_np ))
print ( stack)
arrays_list = np.zeros((3,2,1))
print ( arrays_list)
arrays_list[:] = tag_list[:],images_np[:]
print(arrays_list)


imgpro.nbr_metrics = 2