from Pyro4 import expose

class Solver:
    def __init__(self, workers=None, input_file_name=None, output_file_name=None):
        self.input_file_name = input_file_name
        self.output_file_name = output_file_name
        self.workers = workers

    def solve(self):
        array = self.read_input()
        step = len(array) / len(self.workers)

        # map
        mapped = []
        for i in range(0, len(self.workers)):
            mapped.append(self.workers[i].mymap(i * step, min((i + 1) * step, len(array) - 1), array))


        # reduce
        reduced = self.myreduce(mapped)
        print("Reduce finished: " + str(reduced))

        # output
        self.write_output(reduced)

        print("Job Finished")

    @staticmethod
    @expose
    def mymap(a, b,arr):
        res = 0
        for i in range(a, b+1):
            res += arr[i]
        return res

    @staticmethod
    @expose
    def myreduce(mapped):
        output = 0
        for x in mapped:
            output += x.value
        return output

    def read_input(self):
        f = open(self.input_file_name, 'r')
        arr = f.read().replace('\n','').strip().split()
        for i in range(0, len(arr)):
            arr[i] = int(arr[i])
        return arr
        f.close()

    def write_output(self, output):
        f = open(self.output_file_name, 'w')
        f.write(str(output))
        f.write('\n')
        f.close()