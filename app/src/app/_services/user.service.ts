import { Injectable, OnInit } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';
import { StorageService } from './storage.service';

const API_URL = 'http://localhost:';

@Injectable({
  providedIn: 'root'
})
export class UserService{
  PORT: any

  constructor(private http: HttpClient, private storageService: StorageService) { }

  init(port: any): void {
    this.PORT = port
    console.log(this.PORT)
  }

  getBlockchain(): Observable<any> {
    return this.http.get(API_URL + this.storageService.getPort() + '/api/get_chain', { responseType: 'text' });
  }

  mine(): Observable<any> {
    return this.http.get(API_URL + this.storageService.getPort() +  '/api/mine_block');
  }

  sync(): Observable<any> {
    return this.http.get(API_URL + this.storageService.getPort() +  '/api/replace_chain');
  }

  makeTransaction(sender: string, receiver: string, amount: number): Observable<any> {
    return this.http.post(API_URL + this.storageService.getPort() + '/api/send_transaction', { "sender": sender, "receiver": receiver, "amount": amount })
  }

  join(username: string, port: number): Observable<any> {
    this.init(port)
    return this.http.post(API_URL + this.storageService.getPort() + '/api/join', { "username": username, "port": port });
  }

  connected(): Observable<any> {
    return this.http.get(API_URL + this.storageService.getPort() + '/api/connected');
  }

  getKey(): Observable<any> {
    return this.http.get(API_URL + '/api/get_keys');
  }
}