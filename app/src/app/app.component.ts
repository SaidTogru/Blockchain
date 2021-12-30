import { ThrowStmt } from '@angular/compiler';
import { Component } from '@angular/core';
import { Router, RouterLink } from '@angular/router';
import { StorageService } from './_services/storage.service';
import { UserService } from './_services/user.service';
import * as Highcharts from 'highcharts';

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

  constructor(private userService: UserService, private router: Router, private storageService: StorageService) { }

  ngOnInit(): void {
    this.userService.connected().subscribe(
      data => {
        this.joined = true;
      },
      err => {
        console.log(err)
      })
  }

  join(username: string, port: number){
    console.log(username)
    this.userService.join(username,port).subscribe(
      data => {
        this.joined = true
        this.storageService.saveUser(username)
        this.router.navigate(['/block'])
      },
      err => {
        console.log(err)
      }
    );
  }
}
