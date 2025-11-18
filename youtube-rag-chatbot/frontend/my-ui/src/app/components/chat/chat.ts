import { CommonModule } from '@angular/common';
import { Component, input, output, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Api } from '../../services/api';
import { AskRequest, AskResponse } from '../../models/api-models';

@Component({
  selector: 'app-chat',
  standalone :true,
  imports: [CommonModule, FormsModule], //CommonModule for *ngIf, FormsModule for [(ngModel)]
  templateUrl: './chat.html',
  styleUrl: './chat.scss',
})
export class Chat {
  videoId = input.required<string>();
  question = signal('');
  answer = signal('');
  isAsking = signal(false);
  error = signal('');

  processNewVideo = output<void>() // Emit event when user wants new video
  

  constructor(private apiService : Api) {}

  askQuestion() : void{
    
    if(!this.question().trim()){
      this.error.set("Please enter a Question");
      return;
    }

    if(!this.question().trim()){
      this.error.set("Please enter a Question");
      return;
    }

    this.isAsking.set(true);
    this.answer.set('');
    this.error.set('');

    const request : AskRequest = {
      video_id : this.videoId().trim(),
      question : this.question().trim()
    };

    this.apiService.askQuestion(request).subscribe({
      next : (response : AskResponse) => {
        this.answer.set(response.answer);
        this.isAsking.set(false);
        console.log('API Response : ', response);
      },
      error : (err) => {
        this.error.set('Failed to get answer : ' + err.message);
        this.isAsking.set(false);
        console.log('API Error : ', err);
      }
    })
  }

  newVideo() : void{
    this.processNewVideo.emit();
  }

}
