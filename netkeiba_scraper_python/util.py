def load_url_list(file_path):
    with open(file_path, 'r') as f:
        url_list = f.readlines()
        return url_list
