import Augmentor
p = Augmentor.Pipeline("/home/uclahci/Camiot/ImageAI/applianceDataSet/test/TV")

p.rotate90(probability=0.5)
p.rotate270(probability=0.5)
p.flip_left_right(probability=0.8)
p.flip_top_bottom(probability=0.3)
p.zoom_random(probability=0.3, percentage_area=0.8)


p.sample(200)


