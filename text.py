


#Metamorphic Tests
metamorphic_tests = [
    {
        "paramaters":{"weather":"none"},
        "done":False, 
        
    
    },
    {
        "paramaters":{"weather":"rain"},
        "done":False, 
        
    },
    {
        "paramaters":{"weather":"night"},
        "done":False, 
        
    }
]



def get_current_metamorphic_test_index():
    index =0
    for test in metamorphic_tests:
        # print(test)
        if test['done'] == False:
            return index
        index+=1
    return False

print(metamorphic_tests)
print(get_current_metamorphic_test_index())


thisdict =	{
  "brand": "Ford",
  "model": "Mustang",
  "year": 1964
}

for i in thisdict:
    print
print(thisdict)