//
//  ViewController.m
//  Culture Radio iOS App
//
//  Created by Frederik Riedel on 27.02.15.
//  Copyright (c) 2015 Frederik Riedel. All rights reserved.
//  some icons by http://icons8.com/web-app/402/Pause

#import "MainViewController.h"

@interface MainViewController ()

@property (nonatomic, strong) SPTSession *session;
@property (nonatomic, strong) SPTAudioStreamingController *player;
@property (nonatomic,strong) CLLocationManager *locationManager;
@property (nonatomic,strong) UIImageView *coverView;
@property (nonatomic,strong) UIButton *playPauseButton;
@property (nonatomic,strong) UIButton *nextButton;
@property (nonatomic,strong) UIButton *prevButton;
@property (nonatomic,strong) UILabel *trackInformationLabel;
@property (nonatomic,strong) UIView *solidBackgroundForControls;
@property (nonatomic, strong) MKMapView *mapView;
@property (nonatomic, strong) UIButton *darkShadeMapView;
@property (nonatomic, strong) UILabel *cityLabel;




@end

int currentPlay = 0;
BOOL musicIsPausedByUser = false;

@implementation MainViewController
@synthesize locationManager,playPauseButton,nextButton,trackInformationLabel,mapView,darkShadeMapView,solidBackgroundForControls,prevButton,cityLabel;
- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor=[UIColor blackColor];
    self.title=@"Cultural Radio";
    
    
    mapView = [[MKMapView alloc] initWithFrame:self.view.frame];
    //    mapView.showsUserLocation = YES;
    mapView.mapType = MKMapTypeSatellite;
    mapView.userInteractionEnabled=NO;
    mapView.delegate=self;
    mapView.showsUserLocation=YES;
    //mapView.region = MKCoordinateRegionMake(mapView.centerCoordinate, MKCoordinateSpanMake(10, 10));
    [self.view addSubview:mapView];
    
    darkShadeMapView = [UIButton buttonWithType:UIButtonTypeCustom];
    darkShadeMapView.frame=mapView.frame;
    darkShadeMapView.backgroundColor=[UIColor colorWithRed:0 green:0 blue:0 alpha:0.6];
    [darkShadeMapView addTarget:self action:@selector(showMap) forControlEvents:UIControlEventTouchUpInside];
    [self.view addSubview:darkShadeMapView];
    
    
    self.coverView=[[UIImageView alloc] initWithFrame:CGRectMake(30, self.navigationController.navigationBar.frame.size.height, self.view.frame.size.width-60, self.view.frame.size.width)];
    self.coverView.contentMode = UIViewContentModeScaleAspectFit;
    [self.view addSubview:self.coverView];
    
    
    locationManager = [[CLLocationManager alloc] init];
    locationManager.delegate = self;
    locationManager.distanceFilter = kCLDistanceFilterNone;
    locationManager.desiredAccuracy = kCLLocationAccuracyHundredMeters;
    
    if ([[[UIDevice currentDevice] systemVersion] floatValue] >= 8.0)
        [self.locationManager requestAlwaysAuthorization];
    
    [locationManager startUpdatingLocation];
    
    
    solidBackgroundForControls = [[UIView alloc] initWithFrame:CGRectMake(0, self.coverView.frame.origin.y+self.coverView.frame.size.height, self.view.frame.size.width, 70)];
    
    [self.view addSubview:solidBackgroundForControls];
    
    playPauseButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    //[playPauseButton setTitle:@"▶︎" forState:UIControlStateNormal];
    [playPauseButton setImage:[UIImage imageNamed:@"play.png"] forState:UIControlStateNormal];
    
    playPauseButton.tintColor=[UIColor lightGrayColor];
    [playPauseButton setTitleColor:[UIColor lightGrayColor] forState:UIControlStateNormal];
    
    playPauseButton.frame=CGRectMake(self.view.frame.size.width/2 - 35, 0, 70, 70);
    [playPauseButton addTarget:self action:@selector(playPauseButtonAction) forControlEvents:UIControlEventTouchUpInside];
    [solidBackgroundForControls addSubview:playPauseButton];
    
    
    
    nextButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    [nextButton setImage:[UIImage imageNamed:@"next.png"] forState:UIControlStateNormal];
    nextButton.tintColor=[UIColor lightGrayColor];
    nextButton.frame=CGRectMake(self.view.frame.size.width/2 + 35, 0, 70, 70);
    [nextButton addTarget:self action:@selector(playNextTrack) forControlEvents:UIControlEventTouchUpInside];
    [solidBackgroundForControls addSubview:nextButton];
    
    prevButton = [UIButton buttonWithType:UIButtonTypeRoundedRect];
    [prevButton setImage:[UIImage imageNamed:@"prev.png"] forState:UIControlStateNormal];
    prevButton.tintColor=[UIColor lightGrayColor];
    prevButton.frame=CGRectMake(self.view.frame.size.width/2 - 35 - 70, 0, 70, 70);
    [prevButton addTarget:nil action:nil forControlEvents:UIControlEventTouchUpInside];
    [solidBackgroundForControls addSubview:prevButton];
    
    
    
    [self.view bringSubviewToFront:self.coverView];
    
    
    trackInformationLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, solidBackgroundForControls.frame.origin.y+solidBackgroundForControls.frame.size.height, self.view.frame.size.width, 50)];
    trackInformationLabel.text=@"";
    trackInformationLabel.numberOfLines=-1;
    trackInformationLabel.font=[UIFont systemFontOfSize:20];
    trackInformationLabel.textAlignment=NSTextAlignmentCenter;
    trackInformationLabel.textColor=[UIColor whiteColor];
    [self.view addSubview:trackInformationLabel];
    
    
    cityLabel = [[UILabel alloc] initWithFrame:CGRectMake(0, trackInformationLabel.frame.origin.y+trackInformationLabel.frame.size.height, self.view.frame.size.width, 70)];
    cityLabel.font=[UIFont systemFontOfSize:30];
    cityLabel.textAlignment=NSTextAlignmentCenter;
    cityLabel.textColor = [UIColor whiteColor];
    [self.view addSubview:cityLabel];
    
    
    [[UIApplication sharedApplication] beginReceivingRemoteControlEvents];
    [self becomeFirstResponder];
    
    // Do any additional setup after loading the view, typically from a nib.
}

- (void)mapView:(MKMapView *)map didUpdateUserLocation:(MKUserLocation *)userLocation
{
    MKCoordinateSpan span = MKCoordinateSpanMake(1,1);
    CLLocationCoordinate2D coordinate = map.userLocation.location.coordinate;
    MKCoordinateRegion region = {coordinate, span};
    
    MKCoordinateRegion regionThatFits = [self.mapView regionThatFits:region];
    NSLog(@"Fit Region %f %f", regionThatFits.center.latitude, regionThatFits.center.longitude);
    
    [self.mapView setRegion:regionThatFits animated:YES];
    //    [map setCenterCoordinate:map.userLocation.location.coordinate animated:YES];
}

-(void) showMap {
    [UIView animateWithDuration:0.5
                          delay:0
                        options:UIViewAnimationOptionCurveLinear
                     animations:^{
                         darkShadeMapView.alpha=0;
                         //self.coverView.alpha=0;
                         self.trackInformationLabel.alpha=0;
                         self.coverView.frame=CGRectMake(0, self.view.frame.size.height-70, 70, 70);
                         //               self.playPauseButton.alpha=0;
                         //                 nextButton.alpha=0;
                         solidBackgroundForControls.backgroundColor=[UIColor colorWithRed:0 green:0 blue:0 alpha:0.8];
                         solidBackgroundForControls.frame=CGRectMake(0, self.view.frame.size.height-70, self.view.frame.size.width, 70);
                         
                     }
     
                     completion:^(BOOL finished) {
                         mapView.mapType = MKMapTypeHybrid;
                         mapView.userInteractionEnabled=YES;
                         
                         UIButton *backToMusic = [UIButton buttonWithType:UIButtonTypeCustom];
                         backToMusic.frame = CGRectMake(0, 0, 70, 70);
                         [backToMusic addTarget:self action:@selector(backToMusic) forControlEvents:UIControlEventTouchUpInside];
                         [solidBackgroundForControls addSubview:backToMusic];
                     }];
}

-(void) backToMusic {
    [UIView animateWithDuration:0.5
                          delay:0
                        options:UIViewAnimationOptionCurveLinear
                     animations:^{
                         darkShadeMapView.alpha=1;
                         //self.coverView.alpha=1;
                         self.trackInformationLabel.alpha=1;
                         self.coverView.frame=CGRectMake(30, self.navigationController.navigationBar.frame.size.height, self.view.frame.size.width-60, self.view.frame.size.width);
                         //                         self.playPauseButton.alpha=1;
                         //                         nextButton.alpha=1;
                         solidBackgroundForControls.backgroundColor=[UIColor clearColor];
                         solidBackgroundForControls.frame=CGRectMake(0, self.coverView.frame.origin.y+self.coverView.frame.size.height, self.view.frame.size.width, 70);
                         
                         self.navigationItem.rightBarButtonItem=nil;
                         
                     }
     
                     completion:^(BOOL finished) {
                         mapView.mapType = MKMapTypeSatellite;
                         mapView.userInteractionEnabled=NO;
                     }];
}

- (void)locationManager:(CLLocationManager *)manager didUpdateToLocation:(CLLocation *)newLocation fromLocation:(CLLocation *)oldLocation {
    //NSLog(@"OldLocation %f %f", oldLocation.coordinate.latitude, oldLocation.coordinate.longitude);
    //NSLog(@"NewLocation %f %f", newLocation.coordinate.latitude, newLocation.coordinate.longitude);
}

-(void) playTrackFromSpotifyURI:(NSString *) uri  {
    [SPTRequest requestItemAtURI:[NSURL URLWithString:uri]
                     withSession:self.session
                        callback:^(NSError *error, id object) {
                            
                            if (error != nil) {
                                NSLog(@"***  lookup got error %@", error);
                                return;
                            }
                            
                            [self.player playTrackProvider:(id <SPTTrackProvider>)object callback:^(NSError *error) {
                                NSLog(@"%@",error.description);
                            }];
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
    trackInformationLabel.text=[NSString stringWithFormat:@"%@ \nby %@",[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataTrackName],[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataArtistName]];
    [self updateCoverView];
    
    [playPauseButton setImage:[UIImage imageNamed:@"pause.png"] forState:UIControlStateNormal];
}

-(void)audioStreaming:(SPTAudioStreamingController *)audioStreaming didChangePlaybackStatus:(BOOL)isPlaying {
    if(isPlaying) {
        NSLog(@"playing");
        [playPauseButton setImage:[UIImage imageNamed:@"pause.png"] forState:UIControlStateNormal];
    } else {
        NSLog(@"Not playing");
        [playPauseButton setImage:[UIImage imageNamed:@"play.png"] forState:UIControlStateNormal];
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
   /* if(currentPlay%2==0) {
        [self playTrackFromSpotifyURI:@"spotify:track:3Lmx5EWbES1hOADj13PwO0"];
    } else {
        [self playTrackFromSpotifyURI:@"spotify:track:5KMAn9u1hCxQB6kdqoQONg"];
    }*/
    
    currentPlay++;
    
    dispatch_async(dispatch_get_global_queue(DISPATCH_QUEUE_PRIORITY_DEFAULT, 0),
                   ^{
                       
                       NSURL * url =[NSURL URLWithString:[NSString stringWithFormat:@"http://192.168.137.117:8000/location/lat/%f/long/%f/",locationManager.location.coordinate.latitude,locationManager.location.coordinate.longitude]];
                       
                       NSLog(@"Load New Data Ffrom Server");
                       
                       NSLog(@"%@",[NSString stringWithFormat:@"http://192.168.137.117:8000/location/lat/%f/long/%f/",locationManager.location.coordinate.latitude,locationManager.location.coordinate.longitude]);
                       
                       NSData * data=[NSData dataWithContentsOfURL:url];
                       
                       
                       
                       dispatch_async(dispatch_get_main_queue(),
                                      ^{
                                          if(data) {
                                              NSDictionary *json =[NSJSONSerialization JSONObjectWithData:data options:kNilOptions error:nil];
                                              //NSLog(@"%@",json[@"result"][0][@"uri"]);
                                              NSLog(@"%@",json);
                                              [self playTrackFromSpotifyURI:json[@"result"][currentPlay%(int)[json[@"result"] count]][@"uri"]];
                                              
                                              cityLabel.text = [NSString stringWithFormat:@"%@, %@",json[@"result"][currentPlay%(int)[json[@"result"] count]][@"location"][@"name"],json[@"result"][currentPlay%(int)[json[@"result"] count]][@"location"][@"countryName"]];
                                              
                                              currentPlay++;
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
                              
                              NSMutableDictionary *songInfo = [[NSMutableDictionary alloc] init];
                              
                              void (^finishedRendering)(UIImage *render) = ^void(UIImage *render) {
                                  MPMediaItemArtwork *albumArt = [[MPMediaItemArtwork alloc] initWithImage: render];
                                  
                                  [songInfo setObject:[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataTrackName] forKey:MPMediaItemPropertyTitle];
                                  [songInfo setObject:[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataArtistName] forKey:MPMediaItemPropertyArtist];
                                  [songInfo setObject:[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataAlbumName] forKey:MPMediaItemPropertyAlbumTitle];
                                  
                                  
                                  
                                  [songInfo setObject:albumArt forKey:MPMediaItemPropertyArtwork];
                                  [[MPNowPlayingInfoCenter defaultCenter] setNowPlayingInfo:songInfo];
                              };
                              
                              [CoverImageRenderer renderCoverImageForLocation:self.mapView.region withLocationName:@"Bern" forBandName:[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataArtistName] usingCoverImage:image andCallbackBlock:finishedRendering];
                              
                              
                              
                              self.coverView.image = image;
                              if (image == nil) {
                                  NSLog(@"Couldn't load cover image with error: %@", error);
                              }
                          });
                      });
                  }];
}


@end
