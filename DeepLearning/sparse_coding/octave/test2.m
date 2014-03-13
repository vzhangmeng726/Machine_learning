%sparseAutoencoderCost(theta, visibleSize, hiddenSize, lambda, sparsityParam, beta, data)
sparseAutoencoderCost(ones(22,1) ,
                      4, 
                      2, 
                      0.0001,
                      0.01, 
                      3, 
                      [1 5;0 5;0 5;1 6])
