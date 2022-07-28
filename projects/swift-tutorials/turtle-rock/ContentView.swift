//
//  ContentView.swift
//  Turtle Rock
//
//  Created by Alexa Fazio on 4/10/21.
//  Inspired by Apple's Swift UI Tutorials (https://developer.apple.com/tutorials/swiftui/creating-and-combining-views)
//  Image asset is from Apple's Swift UI Tutorials


import SwiftUI

struct ContentView: View {
    var body: some View {
        VStack {

            VStack {
                Spacer()
                Image("turtlerock")
                    .clipShape(/*@START_MENU_TOKEN@*/Circle()/*@END_MENU_TOKEN@*/)
                    .overlay(Circle().stroke(Color.white, lineWidth: 4))
                    .shadow(radius: /*@START_MENU_TOKEN@*/10/*@END_MENU_TOKEN@*/)
                Spacer()
            }
        
            VStack (alignment: .leading) {

                HStack {
                    Text("Turtle Rock")
                        .font(.title)
                        .fontWeight(.semibold)
                        .padding([.top, .leading, .trailing])
                }
                
                Divider()
                
                HStack {
                    Text("Joshua Tree National Park")
                        
                        .padding(.leading)
                    Spacer()
                    Text("California")
                        .padding(.trailing)
                }
                .font(.subheadline)
                .foregroundColor(.blue)
                
                Text("About Turtle Rock")
                    .fontWeight(.medium)
                    .padding()
                    .font(.headline)
                    .background(Color.white)
                Text("Turtle Rock is a cool rock that is cool very cool indeed. It is awesome.")
                    .padding(.horizontal)
                Spacer()
                
            }
        }
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

