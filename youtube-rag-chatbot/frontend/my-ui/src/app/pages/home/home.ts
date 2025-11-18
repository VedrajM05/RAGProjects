import { Component, signal } from '@angular/core';
import { Chat } from '../../components/chat/chat';
import { VideoProcessor } from '../../components/video-processor/video-processor';
import { CommonModule } from '@angular/common';

@Component({
  selector: 'app-home',
  standalone : true,
  imports: [CommonModule,VideoProcessor, Chat],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {
  // Track if video is processed
  isVideoProcessed = signal(false);
  currentVideoId = signal('')

  //When video is processed, store id and show chat
  onVideoProcessed(videoId : string): void{
    this.currentVideoId.set(videoId);
    this.isVideoProcessed.set(true);
  }

  //Reset for new video
  onNewVideo(): void{
    this.isVideoProcessed.set(false);
    this.currentVideoId.set('');
    
  }

}
