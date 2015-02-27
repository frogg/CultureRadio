//
//  ViewController.m
//  Culture Radio iOS App
//
//  Created by Frederik Riedel on 27.02.15.
//  Copyright (c) 2015 Frederik Riedel. All rights reserved.
//

#import "MainViewController.h"

@interface MainViewController ()

@property (nonatomic, strong) SPTSession *session;
@property (nonatomic, strong) SPTAudioStreamingController *player;
@property (nonatomic,strong) CLLocationManager *locationManager;
@property (nonatomic,strong) UIImageView *coverView;
@property (nonatomic,strong) UIButton *playPauseButton;



@end

@implementation MainViewController
@synthesize locationManager,playPauseButton;
- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor=[UIColor blackColor];
    self.title=@"Cultural Radio";
    
    self.coverView=[[UIImageView alloc] initWithFrame:CGRectMake(0, self.navigationController.navigationBar.frame.size.height, self.view.frame.size.width, self.view.frame.size.width)];
    [self.view addSubview:self.coverView];
    
    
    locationManager = [[CLLocationManager alloc] init];
    locationManager.delegate = self;
    locationManager.distanceFilter = kCLDistanceFilterNone;
    locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters;
    
    if ([[[UIDevice currentDevice] systemVersion] floatValue] >= 8.0)
        [self.locationManager requestAlwaysAuthorization];
    
    [locationManager startUpdatingLocation];
    
    
    playPauseButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    [playPauseButton setTitle:@"▶︎" forState:UIControlStateNormal];
    playPauseButton.frame=CGRectMake(0, self.coverView.frame.origin.y+self.coverView.frame.size.height, self.view.frame.size.width, 100);
    [playPauseButton addTarget:self action:@selector(playPauseButtonAction) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:playPauseButton];
    
    
    
    [[UIApplication sharedApplication] beginReceivingRemoteControlEvents];
    [self becomeFirstResponder];
    
    // Do any additional setup after loading the view, typically from a nib.
}

- (void)locationManager:(CLLocationManager *)manager didUpdateToLocation:(CLLocation *)newLocation fromLocation:(CLLocation *)oldLocation {
    NSLog(@"OldLocation %f %f", oldLocation.coordinate.latitude, oldLocation.coordinate.longitude);
    NSLog(@"NewLocation %f %f", newLocation.coordinate.latitude, newLocation.coordinate.longitude);
}

-(void) play {
    [SPTRequest requestItemAtURI:[NSURL URLWithString:@"spotify:track:7Fng0zvM0XLoMHyINeu8Kj"]
                     withSession:self.session
                        callback:^(NSError *error, id object) {
                            
                            if (error != nil) {
                                NSLog(@"***  lookup got error %@", error);
                                return;
                            }
                            
                            [self.player playTrackProvider:(id <SPTTrackProvider>)object callback:nil];
                        }];
}

-(void) playPauseButtonAction {
    if(self.player.isPlaying) {
        [self.player setIsPlaying:NO callback:nil];
    } else {
        [self.player setIsPlaying:YES callback:nil];
    }
}

- (void)didReceiveMemoryWarning {
    [super didReceiveMemoryWarning];
    // Dispose of any resources that can be recreated.
}

-(void)handleNewSession:(SPTSession *)session {
    self.session = session;
    
    if (self.player == nil) {
        self.player = [[SPTAudioStreamingController alloc] initWithClientId:@kClientId];
        self.player.playbackDelegate = self;
    }
    
    [self.player loginWithSession:session callback:^(NSError *error) {
        
        if (error != nil) {
            NSLog(@"*** Enabling playback got error: %@", error);
            return;
        }
        
        [self playNextTrack];
    }];
}

- (void) audioStreaming:(SPTAudioStreamingController *)audioStreaming didChangeToTrack:(NSDictionary *)trackMetadata {
    NSLog(@"%@",[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataTrackName]);
    [self updateCoverView];
    [playPauseButton setTitle:@"||" forState:UIControlStateNormal];
}

-(void)audioStreaming:(SPTAudioStreamingController *)audioStreaming didChangePlaybackStatus:(BOOL)isPlaying {
    if(isPlaying) {
        NSLog(@"playing");
        [playPauseButton setTitle:@"||" forState:UIControlStateNormal];
    } else {
        NSLog(@"Not playing");
        [playPauseButton setTitle:@"▶︎" forState:UIControlStateNormal];
    }
}


- (void)remoteControlReceivedWithEvent:(UIEvent *)event {
    // If it is a remote control event handle it correctly
    if (event.type == UIEventTypeRemoteControl) {
        if (event.subtype == UIEventSubtypeRemoteControlPlay) {
            [self.player setIsPlaying:YES callback:nil];
        } else if (event.subtype == UIEventSubtypeRemoteControlPause) {
            [self.player setIsPlaying:NO callback:nil];
        } else if (event.subtype == UIEventSubtypeRemoteControlNextTrack) {
            [self playNextTrack];
        }
    }
}

-(void) playNextTrack {
    //temporär
    [self play];
    
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0),
                   ^{
                       
                       NSURL * url =[NSURL URLWithString:[NSString stringWithFormat:@"http://192.168.137.192:8000/location/lat/%f/long/%f/",locationManager.location.coordinate.latitude,locationManager.location.coordinate.longitude]];
                       NSData * data=[NSData dataWithContentsOfURL:url];
                       
                       
                       dispatch_async(dispatch_get_main_queue(),
                                      ^{
                                          if(data) {
                                              NSDictionary *json =[NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:nil];
                                              NSLog(@"%@",json);
                                          } else {
                                              NSLog(@"loading data failed 😭");
                                          }
                                          
                                      });
                   });
    
    
}

-(void) updateCoverView {
    [SPTAlbum albumWithURI:[NSURL URLWithString:[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataAlbumURI]]
                   session:self.session
                  callback:^(NSError *error, SPTAlbum *album) {
                      
                      NSURL *imageURL = album.largestCover.imageURL;
                      if (imageURL == nil) {
                          NSLog(@"Album %@ doesn't have any images!", album);
                          self.coverView.image = nil;
                          return;
                      }
                      
                      // Pop over to a background queue to load the image over the network.
                      dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0), ^{
                          NSError *error = nil;
                          UIImage *image = nil;
                          NSData *imageData = [NSData dataWithContentsOfURL:imageURL options:0 error:&error];
                          
                          if (imageData != nil) {
                              image = [UIImage imageWithData:imageData];
                          }
                          
                          // …and back to the main queue to display the image.
                          dispatch_async(dispatch_get_main_queue(), ^{
                              
                              self.coverView.image = image;
                              if (image == nil) {
                                  NSLog(@"Couldn't load cover image with error: %@", error);
                              }
                          });
                      });
                  }];
}


@end
