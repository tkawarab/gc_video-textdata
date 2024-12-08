from google.cloud import videointelligence
import copy

def create_lang_file(video_file_object):
    annotation_result = load_video_textdetection(video_file_object)
    array_tbl = get_textdetection(annotation_result)
    #print(array_tbl)

def load_video_textdetection_uri(input_uri):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    #video_config = videointelligence.TextDetectionConfig(language_hints=["ja-JP"],model="builtin/latest")
    video_config = videointelligence.TextDetectionConfig(language_hints=["ja-JP"])
    video_context = videointelligence.VideoContext(text_detection_config=video_config)
    features = [videointelligence.Feature.TEXT_DETECTION]
    #operation = video_client.annotate_video(
    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_uri": input_uri,
            "video_context": video_context
        }
    )

    print("\nProcessing video for text detection.")

    
    result = operation.result(timeout=3600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]
    return annotation_result

def load_video_textdetection(video_file_object):
    video_client = videointelligence.VideoIntelligenceServiceClient()
    video_context = videointelligence.VideoContext()
    features = [videointelligence.Feature.TEXT_DETECTION]
    #operation = video_client.annotate_video(
    operation = video_client.annotate_video(
        request={
            "features": features,
            "input_content": video_file_object,
            "video_context": video_context,
        }
    )

    print("\nProcessing video for text detection.")
    result = operation.result(timeout=600)

    # The first result is retrieved because a single video was processed.
    annotation_result = result.annotation_results[0]
    return annotation_result

def get_textdetection(annotation_result):
    array_tbl = []
    array_rec = []
    for text_annotation in annotation_result.text_annotations:
        #print("\nText: {}".format(text_annotation.text))

        # Get the first text segment
        text_segment = text_annotation.segments[0]
        start_time = text_segment.segment.start_time_offset
        end_time = text_segment.segment.end_time_offset
        
        array_rec.append(start_time.seconds + start_time.microseconds * 1e-6)
        array_rec.append(end_time.seconds + end_time.microseconds * 1e-6)
        #print(
        #    "start_time: {}, end_time: {}".format(
        #        start_time.seconds + start_time.microseconds * 1e-6,
        #        end_time.seconds + end_time.microseconds * 1e-6,
        #    )
        #)

        #print("Confidence: {}".format(text_segment.confidence))
        array_rec.append(text_annotation.text)
        array_rec.append(text_segment.confidence)

        # Show the result for the first frame in this segment.
        frame = text_segment.frames[0]
        time_offset = frame.time_offset
        #print(
        #    "Time offset for the first frame: {}".format(
        #        time_offset.seconds + time_offset.microseconds * 1e-6
        #    )
        #)
        array_rec.append(time_offset.seconds + time_offset.microseconds * 1e-6)
        #print("Rotated Bounding Box Vertices:")
        for vertex in frame.rotated_bounding_box.vertices:
            #print("\tVertex.x: {}, Vertex.y: {}".format(vertex.x, vertex.y))
            array_rec.append(vertex.x)
            array_rec.append(vertex.y)
        array_tbl.append(copy.deepcopy(array_rec))
        array_rec.clear()
    return array_tbl