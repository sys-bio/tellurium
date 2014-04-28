import roadrunner
import roadrunner.testing
rr = roadrunner.RoadRunner(roadrunner.testing.getData('feedback.xml'))
result = rr.simulate()
roadrunner.plot(result)
