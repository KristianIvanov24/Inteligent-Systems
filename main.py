import numpy as np


class Neuron:
    def __init__(self):
        self.value = np.inf
        self.delta = np.inf
        self.parents = []
        self.children = []
        self.inputWeights = []


def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))


def activate_neuron(neuron):
    neuron.value = sigmoid(np.sum([p.value * w for p, w in zip(neuron.parents, neuron.inputWeights)]))


def create_neural_network(neuron_distribution, add_bias=True):
    offset = 0
    if add_bias:
        neuron_distribution = [x + 1 for x in neuron_distribution]
        offset = 1

    layers = [[Neuron() for _ in range(neurons)] for neurons in neuron_distribution]

    for i in range(len(layers)):
        if i != len(layers) - 1:
            layers[i][-1].value = -1

        for j in range(len(layers[i])):
            if i == 0 or j == len(layers[i]) - 1:
                layers[i][j].parents = []
            else:
                layers[i][j].parents = layers[i - 1]

            if i == len(layers) - 1:
                layers[i][j].children = []
            else:
                layers[i][j].children = layers[i + 1][:-offset]

            layers[i][j].inputWeights = [np.random.uniform(-0.05, 0.05) for _ in range(len(layers[i][j].parents))]

    layers[-1].pop()
    return layers


def backpropagate(neural_network, input_data, output_data, alpha=0.5):
    hidden_layers = neural_network[1:-1]
    output_layer = neural_network[-1]

    sig_gradient = lambda x: x * (1 - x)

    for i in range(len(output_layer)):
        output_layer[i].delta = (output_data[i] - output_layer[i].value) * sig_gradient(output_layer[i].value)
        for j in range(len(output_layer[i].parents)):
            output_layer[i].inputWeights[j] += alpha * output_layer[i].delta * output_layer[i].parents[j].value

    for i in reversed(range(len(hidden_layers))):
        for j in range(len(hidden_layers[i])):
            temp = np.sum([child.delta * child.inputWeights[j] for child in hidden_layers[i][j].children])
            hidden_layers[i][j].delta = sig_gradient(hidden_layers[i][j].value) * temp
            for k in range(len(hidden_layers[i][j].parents)):
                hidden_layers[i][j].inputWeights[k] += alpha * hidden_layers[i][j].parents[k].value * hidden_layers[i][j].delta


def forward_propagate(neural_network, input_data):
    for j in range(len(neural_network[0]) - 1):
        neural_network[0][j].value = input_data[j]

    for j in range(1, len(neural_network)):
        for k in range(len(neural_network[j])):
            activate_neuron(neural_network[j][k])


def train(neural_network, inputs, outputs, max_iters=50000, err_threshold=0.01):
    for i in range(max_iters):
        for z in range(len(inputs)):
            forward_propagate(neural_network, inputs[z])
            backpropagate(neural_network, inputs[z], [outputs[z]])


if __name__ == '__main__':
    network_input = [[0, 0], [1, 0], [0, 1], [1, 1]]
    network_output_or = [0, 1, 1, 1]
    network_output_and = [0, 0, 0, 1]
    network_output_xor = [0, 1, 1, 0]

    neural_network_or = create_neural_network([2, 2, 1])
    neural_network_and = create_neural_network([2, 2, 1])
    neural_network_xor = create_neural_network([2, 2, 1])

    train(neural_network_or, network_input, network_output_or)
    train(neural_network_and, network_input, network_output_and)
    train(neural_network_xor, network_input, network_output_xor)

    print("OR Results:")
    for test in network_input:
        forward_propagate(neural_network_or, test)
        print(f"Result: {test} -> {neural_network_or[-1][0].value:.6f}")

    print("\nAND Results:")
    for test in network_input:
        forward_propagate(neural_network_and, test)
        print(f"Result: {test} -> {neural_network_and[-1][0].value:.6f}")

    print("\nXOR Results:")
    for test in network_input:
        forward_propagate(neural_network_xor, test)
        print(f"Result: {test} -> {neural_network_xor[-1][0].value:.6f}")