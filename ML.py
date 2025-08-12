import random
import copy


class AI:
    def __init__(self, input, neurons, layers, net=None):
        self.input = input
        self.neurons = neurons
        self.layers = layers
        if net is None:
            self.net = [[[[self.get_random(), self.get_random()] for _ in range(neurons)] for _ in range(neurons)] for _ in range(layers - 1)]
            self.net.insert(0, [[[self.get_random(), self.get_random()] for _ in range(input)] for _ in range(neurons)])
            self.net.append([[[self.get_random(), self.get_random()] for _ in range(neurons)] for _ in range(input)])
        else:
            self.net = net

    def get_random(self):
        return random.random() * 4 - 2

    def play(self, input):
        neuron_net = [[0] * self.neurons for _ in range(self.layers)]
        neuron_net.insert(0, input)
        neuron_net.append([0] * self.input)
        for i in range(self.neurons):
            for j in range(self.input):
                neuron_net[1][i] += neuron_net[0][j] * self.net[0][i][j][0] + self.net[0][i][j][1]
        for l in range(1, self.layers):
            for i in range(self.neurons):
                for j in range(self.neurons):
                    neuron_net[l + 1][i]    += neuron_net[l][j] * self.net[l][i][j][0] + self.net[l][i][j][1]
        for i in range(self.input):
            for j in range(self.neurons):
                neuron_net[-1][i] += neuron_net[-2][j] * self.net[-2][i][j][0] + self.net[-2][i][j][1]
        for i in range(len(neuron_net[-1])):
            if neuron_net[-1][i] < 0:
                neuron_net[-1][i] = 0
        return neuron_net[-1].index(max(neuron_net[-1]))
        # d = sum(neuron_net[-1])
        # if d == 0:
        #     return random.randint(0, self.input - 1)
        # for i in range(self.input):
        #     neuron_net[-1][i] = neuron_net[-1][i] / d
        # rand = random.random()
        # step = 0
        # for i in range(self.input):
        #     if step <= rand <= step + neuron_net[-1][i]:
        #         return i
        #     step += neuron_net[-1][i]
        # return -1

    def mutate(self, learning_rate, another_ai):
        net = copy.deepcopy(self.net)
        for i in range(self.layers):
            for ii in range(len(net[i])):
                for iii in range(len(net[i][ii])):
                    for iv in range(len(net[i][ii][iii])):
                        rand = 1 if random.random() > 0.5 else 0
                        net[i][ii][iii][iv] = self.net[i][ii][iii][iv] * rand + another_ai.net[i][ii][iii][iv] * (1 - rand)
                        net[i][ii][iii][iv] += (random.random() * 2 - 1) * learning_rate if random.random() < 0.2 else 0
        return AI(self.input,self.neurons,self.layers,net=net)

