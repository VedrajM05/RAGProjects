import { Component } from '@angular/core';
import { Chat } from '../../components/chat/chat';
import { VideoProcessor } from '../../components/video-processor/video-processor';

@Component({
  selector: 'app-home',
  standalone : true,
  imports: [VideoProcessor],
  templateUrl: './home.html',
  styleUrl: './home.scss',
})
export class Home {

}
