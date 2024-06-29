class ToyStore:
    def __init__(self):
        #creating toyStore data
        self.toyStore = {
            "Whale":{
                "stock": 0,
                "price": 100
            },
            "Tux":{
                "stock": 10,
                "price": 20
            }
        }
    
    def query(self, request):
        '''
        method is used to query toy and return its price if present else an associated error code 
        '''
        #splitting the request string into query and toyname
        data = request.split(' ')

        #setting default value to return 
        val = -1

        #check if query keyword is sent, if not returns -1 and prints error in query name
        if data[0].upper() != 'QUERY':
            print('Error in query name')
        else:
            #if toyname is found check its stock, and returning price if instock
            if data[1] in self.toyStore:
                if self.toyStore[data[1]]["stock"] > 0:
                    val = self.toyStore[data[1]]["price"]
                else:
                    val = 0
        
        return val