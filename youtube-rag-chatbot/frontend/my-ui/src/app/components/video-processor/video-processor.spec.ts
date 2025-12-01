import { ComponentFixture, TestBed } from '@angular/core/testing';
import { VideoProcessor } from './video-processor';
import { of } from 'rxjs';
import { Api } from '../../services/api';

class MockApiService {
  processVideo(){
    return of({ video_id : '123', status: 'COMPLETED' })
  }
}

describe('VideoProcessor Component', () => {
  let component: VideoProcessor;
  let fixture: ComponentFixture<VideoProcessor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VideoProcessor],
      providers: [
        {provide : Api, useClass : MockApiService}
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(VideoProcessor);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
