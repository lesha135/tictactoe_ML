import random
import copy


class AI():
    def __init__(self, input, neurons,layers, net=None):
        self.input = input
        self.neurons = neurons
        self.layers = layers
        if net is None:
            self.net = [[[[random.random() * 4 - 2, random.random() - 0.5] for _ in range(neurons)] for _ in range(neurons)] for _ in range(layers-1)]
            self.net.insert(0,[[[random.random() * 4 - 2, random.random() - 0.5] for _ in range(input)] for _ in range(neurons)])
            self.net.append([[[random.random() * 4 - 2, random.random() - 0.5] for _ in range(neurons)] for _ in range(input)])
        else:
            self.net = net
    def play(self, input):
        neuron_net = [[0]*self.neurons for _ in range(self.layers)]
        neuron_net.insert(0,input)
        neuron_net.append([0]*self.input)
        for i in range(self.neurons):
            for j in range(self.input):
                neuron_net[1][i] += neuron_net[0][j] * self.net[0][i][j][0] + self.net[0][i][j][1]
        for l in range(1,self.layers):
            for i in range(self.neurons):
                for j in range(self.neurons):
                    neuron_net[l+1][i] += neuron_net[l][j] * self.net[l][i][j][0] + self.net[l][i][j][1]
        for i in range(self.input):
            for j in range(self.neurons):
                neuron_net[-1][i] += neuron_net[-2][j] * self.net[-2][i][j][0] + self.net[-2][i][j][1]
        d = sum(neuron_net[-1])
        for i in range(self.input):
            neuron_net[-1][i] = neuron_net[-1][i] / d
        rand = random.random()
        step = 0
        for i in range(self.input):
            if step <= rand <= step + neuron_net[2][i]:
                return i
            step += neuron_net[2][i]
        return -1

    def evolve(self, copies_num,learning_rate):
        ans = [AI(self.input,self.neurons,self.layers,self.net)]
        for _ in range(copies_num-1):
            net = copy.deepcopy(self.net)
            for i in range(self.neurons):
                for j in range(self.input):
                    net[0][i][j][0] += (random.random()*2-1)*learning_rate
                    net[1][j][i][0] += (random.random()*2-1)*learning_rate
                    net[0][i][j][1] += (random.random()*2-1)*learning_rate/2
                    net[1][j][i][1] += (random.random()*2-1)*learning_rate/2
            ans.append(AI(self.input,self.neurons,self.layers,net))
        return ans
