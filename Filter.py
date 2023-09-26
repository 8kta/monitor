class Filter:
    def __init__(self, filter_list):
        self.filter_list = filter_list

    def accept(self, file_name) -> bool:
        for word in self.filter_list:
            if word.strip() in file_name:
                return False
        return True

    def reject(self, file_name) -> bool:
        for word in self.filter_list:
            if word.strip() in file_name:
                return True
        return False

