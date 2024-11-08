
#################################################
### THIS FILE WAS AUTOGENERATED! DO NOT EDIT! ###͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
#################################################
# file to edit: solution.ipynb͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

import numpy as np
from helper_functions import *

def get_initial_means(array, k):
    """
    Picks k random points from the 2D array
    (without replacement) to use as initial
    cluster means

    params:
    array = numpy.ndarray[numpy.ndarray[float]] - m x n | datapoints x features

    k = int

    returns:
    initial_means = numpy.ndarray[numpy.ndarray[float]]
    """

    if len(array.shape) == 3:
        array = array.reshape(-1, array.shape[-1])
    idx_rand = np.random.choice(array.shape[0],k, replace=False)
    return array[idx_rand]

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def k_means_step(X, k, means):
    """
    A single update/step of the K-means algorithm
    Based on a input X and current mean estimate,
    predict clusters for each of the pixels and
    calculate new means.
    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n | pixels x features (already flattened)
    k = int
    means = numpy.ndarray[numpy.ndarray[float]] - k x n

    returns:
    (new_means, clusters)
    new_means = numpy.ndarray[numpy.ndarray[float]] - k x n
    clusters = numpy.ndarray[int] - m sized vector
    """

    new_means = np.zeros((k,means.shape[1]))

    # Broadcasting setup depending on input shape
    X_broadcast = X[:, np.newaxis, :]

    # Find mean that each data point (pixel) is closest to with broadcasting and euclidean distance
    means = means[np.newaxis,:,:]

    euclidean = np.sqrt(np.sum((X_broadcast - means)**2,axis=2)) # this produces a comparison of each sample (row) in X being compared to each cluster in means

    # Choose the cluster mean that each data is closest to
    clusters = np.argmin(euclidean,axis=1)

    # Reassign each cluster center to the new mean of the data
    for idx in range(k):
        cluster_mask = X[clusters == idx] # get mask of each cluster
        new_means[idx,:] = np.mean(cluster_mask,axis=0)

    return (new_means, clusters)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def k_means_segment(image_values, k=3, initial_means=None):
    """
    Separate the provided RGB values into
    k separate clusters using the k-means algorithm,
    then return an updated version of the image
    with the original values replaced with
    the corresponding cluster values.

    params:
    image_values = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - r x c x ch
    k = int
    initial_means = numpy.ndarray[numpy.ndarray[float]] or None

    returns:
    updated_image_values = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - r x c x ch
    """

    if initial_means is None:
        means = get_initial_means(image_values, k)
    else:
        means = initial_means

    # Flatten image for processing
    flatten_image = image_values.reshape(-1, image_values.shape[-1])

    # Change clusters until there is no more change
    clusters_old = np.zeros_like(flatten_image.shape[0],dtype=int)

    # Loop until the changes stop
    while True:
        (means, clusters) = k_means_step(flatten_image, k, means)
        if np.array_equal(clusters, clusters_old):
            break
        clusters_old = clusters

    # Reform and reshape images
    updated_flattened_image = means[clusters]
    return updated_flattened_image.reshape(image_values.shape)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

"""
Make sure to put #export (first line in this cell) only
if you call/use this function elsewhere in the code
"""
def compute_sigma(X, MU):
    """
    Calculate covariance matrix, based in given X and MU values

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n

    returns:
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    """
    m,n = X.shape
    k,_ = MU.shape

    SIGMA = np.zeros((k,n,n))

    for cluster in range(k):
        diff = X-MU[cluster,:] # find the difference between each data point (row of X) and the mean of each channel (row of MU)
        SIGMA[cluster,:,:] = (diff.T @ diff) / (m-1)

    return SIGMA


########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def initialize_parameters(X, k):
    """
    Return initial values for training of the GMM
    Set component mean to a random
    pixel's value (without replacement),
    based on the mean calculate covariance matrices,
    and set each component mixing coefficient (PIs)
    to a uniform values
    (e.g. 4 components -> [0.25,0.25,0.25,0.25]).

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int

    returns:
    (MU, SIGMA, PI)
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k
    """
    _,n = X.shape
    MU = np.zeros((k,n))

    for cluster in range(k):
        MU_idx = np.random.choice(range(len(X[:,0])),1,replace=False)
        MU[cluster,:] = X[MU_idx,:]

    SIGMA = compute_sigma(X, MU)

    # Initialize the weighting of each gaussian as uniform
    PI = np.ones((k))/k

    return (MU,SIGMA,PI)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def prob(x, mu, sigma):
    """Calculate the probability of x (a single
    data point or an array of data points) under the
    component with the given mean and covariance.
    The function is intended to compute multivariate
    normal distribution, which is given by N(x;MU,SIGMA).

    params:
    x = numpy.ndarray[float] (for single datapoint)
        or numpy.ndarray[numpy.ndarray[float]] (for array of datapoints)
    mu = numpy.ndarray[float]
    sigma = numpy.ndarray[numpy.ndarray[float]]

    returns:
    probability = float (for single datapoint)
                or numpy.ndarray[float] (for array of datapoints)
    """
    n = sigma.shape[-1]

    sigma_inv = np.linalg.inv(sigma)
    sigma_det = np.linalg.det(sigma)
    norm = 1 / np.sqrt((2 * np.pi) ** n * sigma_det)

    if x.ndim == 1:
        x = x[np.newaxis, :]
    diff = x - mu

    exponent = np.exp(-0.5*np.einsum('ij,ij->i',diff @ sigma_inv, diff))

    p = (norm * exponent)

    if len(p) == 1:
        p = float(p)

    return p

    p = np.zeros((x.shape[0]))

    # If one dimensional input, simply calculate probability, otherwise calculate it for each data point
    if len(x.shape) == 1:
        p = 1/np.sqrt(((2*np.pi)**n)*np.linalg.det(sigma))*np.exp((-1/2)*(x-mu) @ np.linalg.inv(sigma) @ (x-mu).T)
    else:
        for idx, x_row in enumerate(x):
            prob_den = 1/np.sqrt(((2*np.pi)**n)*np.linalg.det(sigma))*np.exp((-1/2)*(x_row-mu) @ np.linalg.inv(sigma) @ (x_row-mu).T)
            p[idx] = prob_den

    return p

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def E_step(X,MU,SIGMA,PI,k):
    """
    E-step - Expectation
    Calculate responsibility for each
    of the data points, for the given
    MU, SIGMA and PI.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k
    k = int

    returns:
    responsibility = numpy.ndarray[numpy.ndarray[float]] - k x m
    """
    m,_ = X.shape
    k,_ = MU.shape
    num = np.zeros((k,m))
    den = np.zeros((k,m))

    # Iterate over each cluster mu to calculate responsibility (probabilities of each datapoint being in each gaussian)
    for idx in range(k):
        normal = prob(X,MU[idx],SIGMA[idx])*PI[idx]
        num[idx,:] = normal
        den += normal

    return num/den

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def M_step(X, r, k):
    """
    M-step - Maximization
    Calculate new MU, SIGMA and PI matrices
    based on the given responsibilities.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    r = numpy.ndarray[numpy.ndarray[float]] - k x m
    k = int

    returns:
    (new_MU, new_SIGMA, new_PI)
    new_MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    new_SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    new_PI = numpy.ndarray[float] - k
    """
    m,n = X.shape
    k,_ = r.shape

    # These are just the update equations for the M step: maximizing the likelihood of the data falling under each gaussian

    m_c = np.sum(r,axis=1) # Total responsibility allocated to cluster c
    new_PI = m_c/np.sum(m_c) # Fraction of total data assigned to cluster c
    new_MU = (r @ X)/m_c[:,np.newaxis] # weighted mean of assigned data

    # Weighted covariance of assigned data
    new_SIGMA = np.zeros((k,n,n))
    for cluster in range(k):
        diff = X-new_MU[cluster,:] # find the difference between each data point (row of X) and the mean of each channel (row of MU)
        weighted_diff = diff * r[cluster,:].reshape(-1,1)
        new_SIGMA[cluster,:,:] = (weighted_diff.T @ diff) / m_c[cluster]

    return (new_MU, new_SIGMA, new_PI)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def likelihood(X, PI, MU, SIGMA, k):
    """Calculate a log likelihood of the
    trained model based on the following
    formula for posterior probability:

    log(Pr(X | mixing, mean, stdev)) = sum((i=1 to m), log(sum((j=1 to k),
                                      mixing_j * N(x_i | mean_j,stdev_j))))

    Make sure you are using natural log, instead of log base 2 or base 10.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k
    k = int

    returns:
    log_likelihood = float
    """
    m,n = X.shape
    k,_ = MU.shape
    to_log = np.zeros((m))

    for cluster in range(k):
        to_log += PI[cluster]*prob(X,MU[cluster],SIGMA[cluster])

    return np.sum(np.log(to_log))

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def train_model(X, k, convergence_function, initial_values = None):
    """
    Train the mixture model using the
    expectation-maximization algorithm.
    E.g., iterate E and M steps from
    above until convergence.
    If the initial_values are None, initialize them.
    Else it's a tuple of the format (MU, SIGMA, PI).
    Convergence is reached when convergence_function
    returns terminate as True,
    see default convergence_function example
    in `helper_functions.py`

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int
    convergence_function = func
    initial_values = None or (MU, SIGMA, PI)

    returns:
    (new_MU, new_SIGMA, new_PI, responsibility)
    new_MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    new_SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    new_PI = numpy.ndarray[float] - k
    responsibility = numpy.ndarray[numpy.ndarray[float]] - k x m
    """

    # Initializing convergence parameters
    converged = False
    conv_ctr=1

    # Initialize values if none
    if initial_values is None:
        initial_values = initialize_parameters(X,k)

    MU,SIGMA,PI = initial_values
    new_likelihood = likelihood(X, PI, MU, SIGMA, k)

    # loop EM until convergence
    while not converged:
        old_likelihood = new_likelihood
        responsibility = E_step(X,MU,SIGMA,PI,k)
        MU,SIGMA,PI = M_step(X, responsibility, k)
        new_likelihood = likelihood(X, PI, MU, SIGMA, k)

        # Check if the likelihood has converged with given helper function
        conv_ctr, converged = convergence_function(old_likelihood, new_likelihood,conv_ctr)

    return (MU, SIGMA, PI, responsibility)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def cluster(r):
    """
    Based on a given responsibilities matrix
    return an array of cluster indices.
    Assign each datapoint to a cluster based,
    on component with a max-likelihood
    (maximum responsibility value).

    params:
    r = numpy.ndarray[numpy.ndarray[float]] - k x m - responsibility matrix

    return:
    clusters = numpy.ndarray[int] - m x 1
    """

    # Get the cluster assignment which is max probability of each data point versus cluster
    return np.argmax(r,axis=0)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def segment(X, MU, k, r):
    """
    Segment the X matrix into k components.
    Returns a matrix where each data point is
    replaced with its max-likelihood component mean.
    E.g., return the original matrix where each pixel's
    intensity replaced with its max-likelihood
    component mean. (the shape is still mxn, not
    original image size)

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    k = int
    r = numpy.ndarray[numpy.ndarray[float]] - k x m - responsibility matrix

    returns:
    new_X = numpy.ndarray[numpy.ndarray[float]] - m x n
    """

    clusters = cluster(r)
    new_X = np.zeros_like(X)

    for cluster_idx in range(k):
        new_X[clusters == cluster_idx] = MU[cluster_idx]

    return new_X

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def best_segment(X,k,iters):
    """Determine the best segmentation
    of the image by repeatedly
    training the model and
    calculating its likelihood.
    Return the segment with the
    highest likelihood.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int
    iters = int

    returns:
    (likelihood, segment)
    likelihood = float
    segment = numpy.ndarray[numpy.ndarray[float]]
    """

    best_likelihood = float('-inf')

    for _ in range(iters):
        MU, SIGMA, PI, r = train_model(X, k, default_convergence, initial_values = None)
        new_X = segment(X, MU, k, r)
        log_likelihood = likelihood(new_X, PI, MU, SIGMA, k)

        if log_likelihood > best_likelihood:
            best_likelihood = log_likelihood
            best_segment = new_X

    return (best_likelihood, best_segment)
########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def improved_initialization(X,k):
    """
    Initialize the training
    process by setting each
    component mean using some algorithm that
    you think might give better means to start with,
    based on the mean calculate covariance matrices,
    and set each component mixing coefficient (PIs)
    to a uniform values
    (e.g. 4 components -> [0.25,0.25,0.25,0.25]).

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int

    returns:
    (MU, SIGMA, PI)
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k
    """

    # Iterations to improve initialization
    iters = 75

    initial_values = initialize_parameters(X,k)
    MU,SIGMA,PI = initial_values

    # loop EM to find better starting values
    for _ in range(iters):
        responsibility = E_step(X,MU,SIGMA,PI,k)
        MU,SIGMA,PI = M_step(X, responsibility, k)

    return (MU, SIGMA, PI)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def new_convergence_function(previous_variables, new_variables, conv_ctr,
                             conv_ctr_cap=10):
    """
    Convergence function
    based on parameters:
    when all variables vary by
    less than 10% from the previous
    iteration's variables, increase
    the convergence counter.

    params:
    previous_variables = [numpy.ndarray[float]]
                         containing [means, variances, mixing_coefficients]
    new_variables = [numpy.ndarray[float]]
                    containing [means, variances, mixing_coefficients]
    conv_ctr = int
    conv_ctr_cap = int

    return:
    (conv_crt, converged)
    conv_ctr = int
    converged = boolean
    """
    increase_convergence_ctr = (abs(previous_variables) * 0.9 <
                                abs(new_variables) <
                                abs(previous_variables) * 1.1)

    if increase_convergence_ctr:
        conv_ctr += 1
    else:
        conv_ctr = 0

    return conv_ctr, conv_ctr > conv_ctr_cap

def train_model_improved(X, k, convergence_function, initial_values = None):
    """
    Train the mixture model using the
    expectation-maximization algorithm.
    E.g., iterate E and M steps from
    above until convergence.
    If the initial_values are None, initialize them.
    Else it's a tuple of the format (MU, SIGMA, PI).
    Convergence is reached when convergence_function
    returns terminate as True. Use new_convergence_fuction
    implemented above.

    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    k = int
    convergence_function = func
    initial_values = None or (MU, SIGMA, PI)

    returns:
    (new_MU, new_SIGMA, new_PI, responsibility)
    new_MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    new_SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    new_PI = numpy.ndarray[float] - k
    responsibility = numpy.ndarray[numpy.ndarray[float]] - k x m
    """

    # Initializing convergence parameters
    converged = False
    conv_ctr=1

    # Initialize values if none
    if initial_values is None:
        initial_values = initialize_parameters(X,k)

    MU,SIGMA,PI = initial_values
    new_likelihood = likelihood(X, PI, MU, SIGMA, k)

    # loop EM until convergence
    while not converged:
        old_likelihood = new_likelihood
        responsibility = E_step(X,MU,SIGMA,PI,k)
        MU,SIGMA,PI = M_step(X, responsibility, k)
        new_likelihood = likelihood(X, PI, MU, SIGMA, k)

        # Check if the likelihood has converged with given helper function
        conv_ctr, converged = convergence_function(old_likelihood, new_likelihood,conv_ctr)

    return (MU, SIGMA, PI, responsibility)

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
# Unittest below will check both of the functions at the same time.͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def bayes_info_criterion(X, PI, MU, SIGMA, k):
    """
    See description above
    params:
    X = numpy.ndarray[numpy.ndarray[float]] - m x n
    MU = numpy.ndarray[numpy.ndarray[float]] - k x n
    SIGMA = numpy.ndarray[numpy.ndarray[numpy.ndarray[float]]] - k x n x n
    PI = numpy.ndarray[float] - k
    k = int

    return:
    bayes_info_criterion = int
    """
    m, n = X.shape

    log_likelihood = likelihood(X, PI, MU, SIGMA, k)
    p = (k * (n * (n + 1)) // 2) + (k-1) + (k*n)

    BIC = -2*log_likelihood + p*np.log(m)

    return BIC

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def BIC_likelihood_model_test(image_matrix, comp_means):
    """Returns the number of components
    corresponding to the minimum BIC
    and maximum likelihood with respect
    to image_matrix and comp_means.

    params:
    image_matrix = numpy.ndarray[numpy.ndarray[float]] - m x n
    comp_means = list(numpy.ndarray[numpy.ndarray[float]]) - list(k x n) (means for each value of k)

    returns:
    (n_comp_min_bic, n_comp_max_likelihood)
    n_comp_min_bic = int
    n_comp_max_likelihood = int
    """

    X = image_matrix
    min_BIC = float('inf')
    max_likelihood = float('-inf')
    n_comp_min_bic = 0
    n_comp_max_likelihood = 0

    for k, MU_comp in enumerate(comp_means, start=1):
        # if k==1:
        #     initial_values = None
        # else:
        #     initial_values = (MU,SIGMA,PI)

        MU, SIGMA, PI, responsibility = train_model_improved(X, k, new_convergence_function, initial_values = None)
        log_likelihood = likelihood(X, PI, MU, SIGMA, k)
        BIC = bayes_info_criterion(X, PI, MU, SIGMA, k)

        if log_likelihood > max_likelihood:
            max_likelihood = log_likelihood
            n_comp_max_likelihood = MU_comp.shape[0]

        if BIC < min_BIC:
            min_BIC = BIC
            n_comp_min_bic = MU_comp.shape[0]

    return n_comp_min_bic, n_comp_max_likelihood

########## DON'T WRITE ANY CODE OUTSIDE THE FUNCTION! ################͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄃͏󠄉͏︆͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
##### CODE BELOW IS USED FOR RUNNING LOCAL TEST DON'T MODIFY IT ######͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄃͏󠄉͏︆͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏
################ END OF LOCAL TEST CODE SECTION ######################͏︆͏󠄃͏󠄌͏󠄍͏󠄂͏️͏󠄃͏󠄉͏︆͏︅͏︀͏︋͏︋͏󠄌͏󠄎͏︀͏󠄋͏︊͏󠄏

def return_your_name():
    return "Jacob Blevins"