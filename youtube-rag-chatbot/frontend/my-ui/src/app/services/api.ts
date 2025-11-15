import { Injectable, inject } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

import { ProcessVideRequest, ProcessVideoResponse, AskRequest, AskResponse } from '../models/api-models';

@Injectable({
  providedIn: 'root',
})
export class Api {
  private baseUrl = "http://localhost:8000"

  //inject() replaces old constructor injection which can still work in newer version of angular 20
  private http = inject(HttpClient)


  /*
  Sends youtube url to backend for transcript processing from video
  */
  processVideo(request : ProcessVideRequest) : Observable<ProcessVideoResponse>{
    return this.http.post<ProcessVideoResponse>(
      `${this.baseUrl}/process-video`, 
      request
    );
  }


  askQuestion(request : AskRequest) : Observable<AskResponse>{
    return this.http.post<AskResponse>(
      `${this.baseUrl}/ask_question`, 
      request
    );
  }


}
