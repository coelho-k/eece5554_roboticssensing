imds = imageDatastore('/home/kyle/Downloads/50_overlap', 'FileExtensions', {'.jpg'})

% Read the first image from the image set.
I = readimage(imds, 1);
no = 10000;
thresh = 0.05e+06

% Once done, experiment with tile to try and get features more uniform
% [y, x, m] = harris(I(:, :, 2), 1000, 'tile', [2 2], 'disp');
grayImage = rgb2gray(I);
[y, x, m] = harris(grayImage, no, 'tile', [2 2], 'disp');%, 'thresh', thresh);
points = cornerPoints([x, y]);
for i = 1:no
    points(i).Metric = m(i);
end

[features, points] = extractFeatures(grayImage, points);

% Initialize all the transforms to the identity matrix. Note that the
% projective transform is used here because the building images are fairly
% close to the camera. Had the scene been captured from a further distance,
% an affine transform would suffice.
numImages = numel(imds.Files);
tforms(numImages) = projective2d(eye(3));

% Initialize variable to hold image sizes.
imageSize = zeros(numImages,2);

% Iterate over remaining image pairs
for n = 2:numImages
    
    % Store points and features for I(n-1).
    pointsPrevious = points;
    featuresPrevious = features;
    
    % Read I(n).
    I = readimage(imds, n);
    grayImage = rgb2gray(I);
    
    % Save image size.
    imageSize(n,:) = size(grayImage);
    
    % Detect and extract features for I(n).    
    [y, x, m] = harris(grayImage, no, 'tile', [2 2], 'disp');%, 'thresh', thresh);
    points = cornerPoints([x, y]);
    for i = 1:no
        points(i).Metric = m(i);
    end
    [features, points] = extractFeatures(grayImage, points);
    
    % Find correspondences between I(n) and I(n-1).
    indexPairs = matchFeatures(features, featuresPrevious, 'Unique', true);
    
    matchedPoints = points(indexPairs(:,1), :);
    matchedPointsPrev = pointsPrevious(indexPairs(:,2), :);
    
    % Estimate the transformation between I(n) and I(n-1).
    tforms(n) = estimateGeometricTransform(matchedPoints, matchedPointsPrev,...
        'projective', 'Confidence', 99.99, 'MaxNumTrials', 5000);
    
    % Compute T(n) * T(n-1) * ... * T(1)
    tforms(n).T = tforms(n).T * tforms(n-1).T; 
  
end

% Compute the output limits  for each transform
for i = 1:numel(tforms)           
    [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imageSize(i,2)], [1 imageSize(i,1)]);    
end

avgXLim = mean(xlim, 2);

[~, idx] = sort(avgXLim);

centerIdx = floor((numel(tforms)+1)/2);

centerImageIdx = idx(centerIdx);

Tinv = invert(tforms(centerImageIdx));

for i = 1:numel(tforms)    
    tforms(i).T = tforms(i).T * Tinv.T;
end

for i = 1:numel(tforms)           
    [xlim(i,:), ylim(i,:)] = outputLimits(tforms(i), [1 imageSize(i,2)], [1 imageSize(i,1)]);
end

for i = 1:5
    middle_x(i) = (xlim(i, 1) + xlim(i, 2)) / 2
    middle_y(i) = (ylim(i, 1) + ylim(i, 2)) / 2
end

%plot(middle_x, middle_y)

maxImageSize = max(imageSize);

% Find the minimum and maximum output limits 
xMin = min([1; xlim(:)]);
xMax = max([maxImageSize(2); xlim(:)]);

yMin = min([1; ylim(:)]);
yMax = max([maxImageSize(1); ylim(:)]);

% Width and height of panorama.
width  = round(xMax - xMin);
height = round(yMax - yMin);

% Initialize the "empty" panorama.
panorama = zeros([height width 3], 'like', I);

blender = vision.AlphaBlender('Operation', 'Binary mask', ...
    'MaskSource', 'Input port');  

% Create a 2-D spatial reference object defining the size of the panorama.
xLimits = [xMin xMax];
yLimits = [yMin yMax];
panoramaView = imref2d([height width], xLimits, yLimits);

% Create the panorama.
for i = 1:numImages
    
    I = readimage(imds, i);   
   
    % Transform I into the panorama.
    warpedImage = imwarp(I, tforms(i), 'OutputView', panoramaView);
                  
    % Generate a binary mask.    
    mask = imwarp(true(size(I,1),size(I,2)), tforms(i), 'OutputView', panoramaView);
    
    % Overlay the warpedImage onto the panorama.
    panorama = step(blender, panorama, warpedImage, mask);
end

figure
imshow(panorama)

