class ResourceHandler():
    document_path = "insert document path here"
    document = None
    
    '''
        Initialize the various resources reading the file
        It considers only the resources with a data antecedent to the
        specified one. 
        If no data is specified, it consider all the resources.
        
    '''
    def init(data = None):
        pass
    
    '''
        Read the last time that a certain resource has been scraped
    '''
    def read_last_time_scraped(src):
        pass
    
    '''
        Update the last time that a certain resource has been scraped with 
        a specified one.
        If missing, it consider the current data.

    '''
    def update_last_time_scraped(src, data = None):
        pass
    