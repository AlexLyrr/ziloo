import pybgs as bgs # This package is manually added

# bg_process = bgs.StaticFrameDifference()
bg_process = bgs.FrameDifference()
# bg_process = bgs.WeightedMovingMean()
# bg_process = bgs.WeightedMovingVariance()
# bg_process = bgs.AdaptiveBackgroundLearning()


def background_removal(frame):
    img_output = bg_process.apply(frame)
    img_bgmodel = bg_process.getBackgroundModel()
    return img_output
