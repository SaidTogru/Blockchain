import { Component, OnInit } from '@angular/core';
import { StorageService } from '../_services/storage.service';
import { UserService } from '../_services/user.service';

@Component({
  selector: 'app-transaction',
  templateUrl: './transaction.component.html',
  styleUrls: ['./transaction.component.scss']
})
export class TransactionComponent implements OnInit {
  pubkey: any;
  string1: any = "b'-----BEGIN PUBLIC KEY-----\n"
  string2: any = "\n-----END PUBLIC KEY-----'"
  content?: string;
  blockchain?: string;
  sender: any = '';
  receiver: string = '';
  amount: number = 0;
  balance: number = 0;

  constructor(private userService: UserService, private storageService: StorageService) { }

  ngOnInit(): void {
    this.getKey()
    this.userService.getBalance().subscribe(
      data => {
        this.balance = data
      },
      err => {
        this.content = JSON.parse(err.error).message
      }
    );
    this.sender = this.storageService.getUser()
    console.log(this.sender)
    this.userService.getBlockchain().subscribe(
      data => {
        this.blockchain = data;
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    );
  }

  transaction(): void {
    this.userService.makeTransaction(this.sender, this.receiver, this.amount).subscribe(
      data => {
        console.log(data)
        this.content = JSON.stringify(data)
      },
      err => {
        this.content = JSON.parse(err.error).message;
      }
    )
  }

  getKey(): void {
    this.userService.getKey().subscribe(
      data =>{
        this.pubkey = data.publickey
        this.pubkey = this.pubkey.replace("b'-----BEGIN PUBLIC KEY-----\\n","")
        this.pubkey = this.pubkey.replace("\\n-----END PUBLIC KEY-----'","")

      },
      err => {
        console.log(err)
      }
    )
  }

}
