from cs231n.classifiers.fc_net_hack_layer_level import *
from cs231n.data_utils import get_CIFAR10_data
from cs231n.gradient_check import eval_numerical_gradient, eval_numerical_gradient_array
from cs231n.solver import Solver

import time
import numpy as np

def rel_error(x, y):
  """ returns relative error """
  return np.mean(np.abs(x - y) / (np.maximum(1e-8, np.abs(x) + np.abs(y))))

data = get_CIFAR10_data()
for k, v in data.iteritems():
  print '%s: ' % k, v.shape

def Test_Affine_Forward():
  # Test the affine_forward function
  num_inputs = 2
  input_shape = (4, 5, 6)
  output_dim = 3
  
  input_size = num_inputs * np.prod(input_shape)
  weight_size = output_dim * np.prod(input_shape)
  
  x = np.linspace(-0.1, 0.5, num=input_size).reshape(num_inputs, *input_shape)
  w = np.linspace(-0.2, 0.3, num=weight_size).reshape(np.prod(input_shape), output_dim)
  b = np.linspace(-0.3, 0.1, num=output_dim)
  
  out, _ = affine_forward(x, w, b)
  correct_out = np.array([[ 1.49834967,  1.70660132,  1.91485297],
                            [ 3.25553199,  3.5141327,   3.77273342]])
  
  # Compare your output with ours. The error should be around 1e-9.
  print 'Testing affine_forward function:'
  print 'difference: ', rel_error(out, correct_out)

def Test_Affine_Backward():
  # Test the affine_backward function

  x = np.random.randn(10, 2, 3)
  w = np.random.randn(6, 5)
  b = np.random.randn(5)
  dout = np.random.randn(10, 5)
  
  dx_num = eval_numerical_gradient_array(lambda x: affine_forward(x, w, b)[0], x, dout)
  dw_num = eval_numerical_gradient_array(lambda w: affine_forward(x, w, b)[0], w, dout)
  db_num = eval_numerical_gradient_array(lambda b: affine_forward(x, w, b)[0], b, dout)
  
  _, cache = affine_forward(x, w, b)
  dx, dw, db = affine_backward(dout, cache)
  
  # The error should be around 1e-10
  print 'Testing affine_backward function:'
  print 'dx error: ', rel_error(dx_num, dx)
  print 'dw error: ', rel_error(dw_num, dw)
  print 'db error: ', rel_error(db_num, db)


def Relu_Forward():
  # Test the relu_forward function
  x = np.linspace(-0.5, 0.5, num=12).reshape(3, 4)
  
  out, _ = relu_forward(x)
  correct_out = np.array([[ 0.,          0.,          0.,          0.,        ],
                          [ 0.,          0.,          0.04545455,  0.13636364,],
                          [ 0.22727273,  0.31818182,  0.40909091,  0.5,       ]])
  
  # Compare your output with ours. The error should be around 1e-8
  print 'Testing relu_forward function:'
  print 'difference: ', rel_error(out, correct_out)

def Relu_Backward():
  x = np.random.randn(10, 10)
  dout = np.random.randn(*x.shape)
  
  dx_num = eval_numerical_gradient_array(lambda x: relu_forward(x)[0], x, dout)
  
  _, cache = relu_forward(x)
  dx = relu_backward(dout, cache)
  
  # The error should be around 1e-12
  print 'Testing relu_backward function:'
  print 'dx error: ', rel_error(dx_num, dx)

def Test_Test_Forward():
  test_sum_forward()

def Test_SVM():
  num_classes, num_inputs = 10, 50
  x = 0.001 * np.random.randn(num_inputs, num_classes)
  y = np.random.randint(num_classes, size=num_inputs)
  mode = 'cpu'
  
  dx_num = eval_numerical_gradient(lambda x: svm_loss(x, y, mode)[0], x, verbose=False)
  loss, dx = svm_loss(x, y, mode)
  
  # Test svm_loss function. Loss should be around 9 and dx error should be 1e-9
  print 'Testing svm_loss:'
  print 'loss: ', loss
  print 'numerical error: ', dx_num
  print 'analytical error: ', dx
  # Note: relative error would we large, because numeriacal error is unstable in gpu mode.
  print 'dx error: ', rel_error(dx_num, dx)
 

def Test_SVM_CPU_GPU():
  num_classes, num_inputs = 10, 50
  x = 0.001 * np.random.randn(num_inputs, num_classes)
  y = np.random.randint(num_classes, size=num_inputs)
  
  loss, dx_cpu = svm_loss(x, y, 'cpu')
  loss, dx_gpu = svm_loss(x, y, 'gpu')
  
  # Test svm_loss function. Loss should be around 9 and dx error should be 1e-9
  print 'Testing svm_loss:'
  print 'loss: ', loss
  print 'dx error: ', rel_error(dx_cpu, dx_gpu)

def Test_Softmax():
  num_classes, num_inputs = 10, 50
  x = 0.001 * np.random.randn(num_inputs, num_classes)
  y = np.random.randint(num_classes, size=num_inputs)

  #dx_num = eval_numerical_gradient(lambda x: softmax_loss(x, y)[0], x, verbose=False)
  loss, dx = softmax_loss(x, y)
  
  # Test softmax_loss function. Loss should be 2.3 and dx error should be 1e-8
  print 'Testing softmax_loss:'
  print 'loss: ', loss
  #print 'dx error: ', rel_error(dx_num, dx)

#Test_Affine_Forward()
#Test_Affine_Backward()
#Relu_Forward()
#Relu_Backward()
#Test_SVM()
#Test_SVM_CPU_GPU()
Test_Softmax()
#Test_Test_Forward()