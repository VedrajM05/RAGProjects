import { CommonModule } from '@angular/common';
import { Component, signal } from '@angular/core';
import { FormsModule } from '@angular/forms';
import { Api } from '../../services/api';

@Component({
  selector: 'app-video-processor',
  imports: [CommonModule, FormsModule],
  templateUrl: './video-processor.html',
  styleUrl: './video-processor.scss',
})
export class VideoProcessor {
  ytURL = signal('');
  message = signal('');
  error = signal('');
  isLoading = signal(false);
  
  constructor(private apiService : Api) {}

  processVideo() : void{
      
  
      if(!this.ytURL().trim()){
        console.log(this.ytURL())
        this.message.set("Please enter a valid Youtube URL");
        return;
      }
      this.isLoading.set(true);
      this.message.set("Processing video, please wait....");
      
      
      this.apiService.processVideo({url : this.ytURL().trim()}).subscribe({
        next : (response) => {
          this.message.set(`Success! Video Id : ${response.video_id} Status : ${response.status}`);
          this.isLoading.set(false);
          console.log('API Response : ', response);
        },
        error : (err) => {
          this.message.set(`Error : ${err.message}`);
          this.isLoading.set(false);
          console.log('API Error : ', err);
        }
      })
    }

}
