import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { UserService } from './_services/user.service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent {
  title = 'app';
  content?: string;
  blockchain?: any;
  user: string = '';
  port: number = 0;
  joined: boolean = false;

  constructor(private userService: UserService, private router: Router) { }

  ngOnInit(): void {
  
  }

  join(username: string, port: number){
    this.userService.join(username,port).subscribe(
      data => {
        this.joined = true
        this.router.navigate(['/block'])
      },
      err => {
        console.log(err)
      }
    );
  }
}
