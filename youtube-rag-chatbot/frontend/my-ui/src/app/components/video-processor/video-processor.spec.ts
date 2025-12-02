import { ComponentFixture, TestBed } from '@angular/core/testing';
import { VideoProcessor } from './video-processor';
import { of } from 'rxjs';
import { Api } from '../../services/api';
import { By } from '@angular/platform-browser';

class MockApiService {
  processVideo(){
    return of({ video_id : '123', status: 'COMPLETED' })
  }
}

describe('VideoProcessor Component', () => {
  let componentVideoProcessor: VideoProcessor;
  let fixture: ComponentFixture<VideoProcessor>;

  beforeEach(async () => {
    await TestBed.configureTestingModule({
      imports: [VideoProcessor],
      providers: [
        {provide : Api, useClass : MockApiService}
      ]
    }).compileComponents();

    fixture = TestBed.createComponent(VideoProcessor);
    componentVideoProcessor = fixture.componentInstance;
    fixture.detectChanges();
  });

  //
  //Check if component is getting created
  //
  it('should create', () => {
    expect(componentVideoProcessor).toBeTruthy(); //basic sanity test to confirm the component initializes correctly
  });

  //
  //check if message signal is set when URL is empty
  //
  it('should set message when URL is empty', () => {
    //Arrange : ensure ytURL is empty
    componentVideoProcessor.ytURL.set('');

    //Act : call method to be tested
    componentVideoProcessor.processVideo();

    //Assert : message signal to be populated
    expect(componentVideoProcessor.message()).toBe('Please enter a valid Youtube URL');
  });

  //
  //Simulate a real button click in the template and verify that it triggers processVideo()
  //
  it('should call processVideo() method, when process video button is clicked', () => {
    //set this ytURL variable, else button is disabled and test fails
    componentVideoProcessor.ytURL.set('https://youtube.com/watch?v=abc123');
    fixture.detectChanges(); //this updates the template with ytURL value

    //Arrange : spy on component VideoProcessor processVideo() method
    const spy = spyOn(componentVideoProcessor, 'processVideo')

    //Find the process video button
    const buttonDebug = fixture.debugElement.query(By.css('.process-btn'));
    const button : HTMLButtonElement = buttonDebug.nativeElement;

    //Assert : precondition : button is clicked
    expect(button.disabled).toBeFalse();

    //Act : simulate a click
    buttonDebug.triggerEventHandler('click', new Event('click'));
    fixture.detectChanges()

    //Assert : processVideo()  should be called
    expect(spy).toHaveBeenCalled();
  });

});
