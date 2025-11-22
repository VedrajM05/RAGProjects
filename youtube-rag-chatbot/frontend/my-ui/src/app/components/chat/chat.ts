import { CommonModule } from '@angular/common';
import { Component, ElementRef, input, output, signal, viewChild, ViewChild, AfterViewChecked } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Api } from '../../services/api';
import { AskRequest, AskResponse } from '../../models/api-models';

// Chat Message Interface
interface ChatMessage{
  type : 'user' | 'assistant';
  content : string;
  timestamp : Date;
}

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
  messages = signal<ChatMessage[]>([]); //for chat messages array
  isAsking = signal(false);
  error = signal('');

  processNewVideo = output<void>() // Emit event when user wants new video
  
  //viewChild() is the Angular-safe way to access the DOM
  private chatContainer = viewChild<ElementRef>('chatContainer')

  constructor(private apiService : Api) {}

  //Auto scroll life cycle hook
  ngAfterViewChecked() : void{
    this.scrollToBottom();
  }

  //auto scrolling logic
  private scrollToBottom() : void {
    const container = this.chatContainer()?.nativeElement;
    if(container){
      container.scrollTop = container.scrollHeight
    }
  }

  askQuestion() : void{
    
    if(!this.question().trim()){
      this.error.set("Please enter a Question");
      return;
    }

    if(!this.question().trim()){
      this.error.set("Please enter a Question");
      return;
    }
    const userQuestion = this.question().trim()

    //adds user message to chat history
    this.addMessage('user', userQuestion);
    this.isAsking.set(true);
    // this.answer.set('');
    this.error.set('');

    const request : AskRequest = {
      video_id : this.videoId().trim(),
      question : this.question().trim()
    };

    this.apiService.askQuestion(request).subscribe({
      next : (response : AskResponse) => {
        //Add assistant message to chat history
        this.addMessage('assistant', response.answer);
        // this.answer.set(response.answer);
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

  private addMessage(type : 'user' | 'assistant', content : string) : void{
    this.messages.update(messages => [
      ...messages,
      {type, content, timestamp : new Date() }
    ]);
  }

  newVideo() : void{
    //clear chat history on new video
    this.messages.set([]);
    this.question.set('');
    this.error.set('')
    this.processNewVideo.emit();
  }

}
