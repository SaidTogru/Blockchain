import { Component, OnInit } from '@angular/core';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-home',
  templateUrl: './home.component.html',
  styleUrls: ['./home.component.scss']
})
export class HomeComponent implements OnInit {
  content?: string;
  blockchain?: any;
  user: string = '';
  port: number = 0;
  joined: boolean = false;

  constructor(private userService: UserService) { }

  ngOnInit(): void {
    this.userService.getBlockchain().subscribe(
      data => {
        this.content = data;
        this.blockchain = JSON.parse(data).chain
        console.log(this.blockchain)
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    );
  }

  join(username: string, port: number){
    this.userService.join(username,port).subscribe(
      data => {
        this.joined = true
      },
      err => {
        console.log(err)
      }
    );
  }
}