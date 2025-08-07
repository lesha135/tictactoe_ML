import random
import copy


class AI():
    def __init__(self, input, neurons, net=None):
        self.input = input
        self.neurons = neurons
        if net is None:
            self.net = [[[(random.random() * 4 - 2) for _ in range(input)] for _ in range(neurons)],
                        [[(random.random() * 4 - 2) for _ in range(neurons)] for _ in range(input)]]
        else:
            self.net = net

    def play(self, input):
        neuron_net = [input, [0] * self.neurons, [0] * self.input]
        for i in range(self.neurons):
            for j in range(self.input):
                neuron_net[1][i] += neuron_net[0][j] * self.net[0][i][j]
        for i in range(self.input):
            for j in range(self.neurons):
                neuron_net[2][i] += neuron_net[1][j] * self.net[1][i][j]
        d = sum(neuron_net[2])
        for i in range(self.input):
            neuron_net[2][i] = neuron_net[2][i] / d
        rand = random.random()
        step = 0
        for i in range(self.input):
            if step <= rand <= step + neuron_net[2][i]:
                return i
            step += neuron_net[2][i]
        return -1

    def evolve(self, copies_num,learning_rate):
        ans = [self.net]
        for _ in range(copies_num-1):
            net = copy.deepcopy(self.net)
            for i in range(self.neurons):
                for j in range(self.input):
                    net[0][i][j] += (random.random()*2-1)*learning_rate
                    net[1][j][i] += (random.random()*2-1)*learning_rate
            ans.append(net)

