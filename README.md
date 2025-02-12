## Aircraft Recognition service

### Recognition model

Satellite Images were collected on GoogleEarth Pro at various time and locations

The dataset was created on Roboflow and is publicly available at: https://universe.roboflow.com/pvaircraftreco/aircraft-reco-1/dataset/2

The dataset was annotated on Roboflow using [bounding boxes](https://docs.roboflow.com/annotate/annotation-tools#bounding-boxes-vs.-polygons).

The model was subsequently trained using YOLOv11 object detection (Fast).

### Attributes

Annotation was done "on the fly". Types were created based on the most recognizable types of aircraft. 
But it lacks consistency at this stage.

We tried to identify different types of aircraft:

- multirole: Su-27/30/34, Mig-29/35 and variants
- bomber: mainly Tu-22M3 at this point, more thorough examination is needed regarding Tu-160
- tu-95: very recognizable as such so an "ad hoc" type was created for the Bear
- trainer: straight wing aircrafts
- unknown swept wing: probably SU-24M
- transport: multi-engine aircrafts
- SU-57: need more examination but an "ad hoc" type was created for the Felon
- helo: Mi-8, Ka-50
- civilian

### Performance

More on that later...
https://blog.roboflow.com/mean-average-precision

![image](https://github.com/user-attachments/assets/206ae31a-35e0-4d5f-864a-38fd4e4772f5)

![image](https://github.com/user-attachments/assets/accb3471-1858-4cfc-9ef5-9d70749d3c11)





