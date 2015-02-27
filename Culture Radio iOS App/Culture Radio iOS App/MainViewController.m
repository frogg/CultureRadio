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

@end

@implementation MainViewController

- (void)viewDidLoad {
    [super viewDidLoad];
    self.view.backgroundColor=[UIColor whiteColor];
    self.title=@"Cultural Radio";
    
    UIButton *playMusic = [[UIButton alloc] init];
    
    // Do any additional setup after loading the view, typically from a nib.
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
        
        [SPTRequest requestItemAtURI:[NSURL URLWithString:@"spotify:track:1E0j1mSM23Iw9hcPVq3wOd"]
                         withSession:session
                            callback:^(NSError *error, id object) {
                                
                                if (error != nil) {
                                    NSLog(@"*** Album lookup got error %@", error);
                                    return;
                                }
                                
                                
                                
                                [self.player playTrackProvider:(id <SPTTrackProvider>)object callback:nil];
                                
                                
                            }];
    }];
}

- (void) audioStreaming:(SPTAudioStreamingController *)audioStreaming didChangeToTrack:(NSDictionary *)trackMetadata {
    NSLog(@"%@",[self.player.currentTrackMetadata valueForKey:SPTAudioStreamingMetadataTrackName]);
}

@end
