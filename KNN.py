import numpy as np

class KNN:
    def __init__(self,max_distance=1, nbr_voisins=3,nbr_metric=3):
        self.__nbr_voisins = nbr_voisins
        self.__nbr_metrics = nbr_metric
        self.__nbr_elements = 0
        self.__max_distance = max_distance
        self.__private = True
        self.__resized = False
        
#private function

    def __resize(self):
        if ( self.__resized):
            del(self.__espace_solution)
            del(self.__tab_distance)
        self.__espace_solution = np.zeros((self.__nbr_elements,self.__nbr_metrics+1))
        self.__tab_distance = np.empty((self.__nbr_elements, 2))
        self.__resized = True

    def __clear(self):
        self.espace_solution[:] =0

    def __calcule_distance(self,point_comparaison):
        if ( self.__resized):
            self.__tab_distance[:, 0] =  np.sum( ((self.__espace_solution[:, 0:self.__nbr_metrics] -point_comparaison)**2),axis=1)**0.5
            self.__tab_distance[:, 1] =  self.__espace_solution[:, -1]
            tab_indices =self.__tab_distance[:, 0].argsort()
            tab_indices_trier = tab_indices[:self.nbr_voisins]
            return self.__tab_distance[tab_indices_trier]


    def __determiner_type(self,resultat):

        resultats = resultat[resultat[:,0]<self.__max_distance]

        indexes = resultat[:,1].astype(int)
        print(indexes)
        counts = np.bincount(indexes)
        print( counts)
        plusfrequents = np.argpartition(-counts, kth=2)[:2]
        print( plusfrequents)
        if ( len(plusfrequents)== 2):
          if (counts[plusfrequents[0]] == counts[plusfrequents[1]]):
            return resultats[0][1] # 2 plus frequent, on prend le plus proche    
          else:
            return resultats[plusfrequents[0]][1] # 1 plus frequent on prend lui
        else:
            return resultats[0][1]  # pas 2 frequents, on prend le plus proche
  
        
        
       

        
                #public functions
    @property
    def nbr_voisins(self):
        return self.__nbr_voisins

    @nbr_voisins.setter
    def nbr_voisins(self,value):
        self.__nbr_voisins = value
        
    @property
    def max_distance(self):
        return self.__max_distance

    @max_distance.setter
    def max_distance(self,value):
        self.__max_distance = value
        
        
    @property
    def nbr_metrics(self):
        return self.__nbr_metrics


    @nbr_metrics.setter
    def nbr_metrics(self,value):
        self.__nbr_metrics = value
        self.__resize()
        
    @property
    def nbr_elements(self):
        return self.__nbr_elements

    @nbr_elements.setter
    def nbr_elements(self,value):
        self.__nbr_elements = value
        self.__resize()    

    @property
    def espace_solution(self):
        return self.__espace_solution


    def rajouter_image_a_espace_solution(self,images_a_ajouter):
        self.nbr_elements = len(images_a_ajouter)
        self.__espace_solution = images_a_ajouter


    def algo_knn(self,image):
        resultat =self.__calcule_distance(image)
        typ = self.__determiner_type(resultat)
        return typ

       
       

   
        
knn = KNN()
images_a_ajouter = np.array(
    [
        [1,2,1,1],
        [1,4,1,1],
        [1,1,7,2],
        [1,3,1,3],
        [1,1,8,1]
        ]
        )
#knn.rajouter_image_a_espace_solution(images_a_ajouter)
#point = np.array([1,4,6])
#knn.calcule_distance(point)        
knn.max_distance = 2
print(knn.max_distance)

        


        


