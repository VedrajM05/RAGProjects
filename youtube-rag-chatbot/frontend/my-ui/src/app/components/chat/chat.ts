import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
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
  videoId = signal('');
  question = signal('');
  answer = signal('');
  isLoading = signal(false);
  error = signal('');

  
  constructor(private apiService : Api) {}

  askQuestion() : void{
    this.error.set('');
    this.answer.set('');

    if(!this.videoId().trim()){
      this.error.set("Please enter a Video Id");
      return;
    }

    if(!this.question().trim()){
      this.error.set("Please enter a Question");
      return;
    }

    this.isLoading.set(true);

    const request : AskRequest = {
      video_id : this.videoId().trim(),
      question : this.question().trim()
    };

    this.apiService.askQuestion(request).subscribe({
      next : (response : AskResponse) => {
        this.answer.set(response.answer);
        this.isLoading.set(false);
        console.log('API Response : ', response);
      },
      error : (err) => {
        this.error.set('Failed to get answer' + err.message);
        this.isLoading.set(false);
        console.log('API Error : ', err);
      }
    })
  }

}
