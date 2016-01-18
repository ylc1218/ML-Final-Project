function cluster = KmeansClustering(X, k)
    
    center = initCenter(X, k);

    %kmeans iteration
    newCenter = zeros(size(center));
    newCluster = zeros(length(X), 1);
    cluster = ones(length(X), 1);
 
    while ~isequal(cluster, newCluster)
        cluster = newCluster;
        
        distMat = pdist2(center, X);
        [~, index] = min(distMat);
        
        for i = 1:k
            newCenter(i, :) = mean( X(index == i, :) );
        end

        center = newCenter;
        newCluster = index;
    end
    
    function center = initCenter(data, k)
        num = length(data);
        center = data(randsample(num, k), :);
    end

end