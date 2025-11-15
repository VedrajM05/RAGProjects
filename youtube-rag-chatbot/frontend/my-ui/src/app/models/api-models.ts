//Interface for processing a video request
export interface ProcessVideRequest{
    url : string;
}


//Interface for processing a video response
export interface ProcessVideoResponse{
    video_id : string;
    status : string;
    message? : string; //optional message from backend, for error or info
}


//Interface for asking questions
export interface AskRequest{
    video_id : string;
    question : string; //actual question text
}


//Interface for processing a video request
export interface AskResponse{
    answer : string
}


