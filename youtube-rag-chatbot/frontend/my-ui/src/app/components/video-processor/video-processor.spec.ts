import { ComponentFixture, TestBed } from '@angular/core/testing';

import { VideoProcessor } from './video-processor';

describe('VideoProcessor', () => {
  let component: VideoProcessor;
  let fixture: ComponentFixture<VideoProcessor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VideoProcessor]
    })
    .compileComponents();

    fixture = TestBed.createComponent(VideoProcessor);
    component = fixture.componentInstance;
    fixture.detectChanges();
  });

  it('should create', () => {
    expect(component).toBeTruthy();
  });
});
