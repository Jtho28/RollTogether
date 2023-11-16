import SwiftUI

struct ContentView: View {
    @State private var selectedPickupLocation = "Scott Campus"
    @State private var selectedDropoffLocation = "Scott Campus"

    var body: some View {
        NavigationView {
            VStack(spacing: 20) {
                NavigationLink(destination: ProfileView()) {
                    RideSharingButton(title: "Profile")
                }

                NavigationLink(destination: ViewRidesView()) {
                    RideSharingButton(title: "View Rides")
                }

                NavigationLink(destination: ManageRidesView()) {
                    RideSharingButton(title: "Manage Rides")
                }

                VStack {
                    Text("Pick-Up Location:")
                    Picker("Pick-Up", selection: $selectedPickupLocation) {
                        ForEach(["Scott Campus", "Dodge Campus", "Aksarben Village", "Village Pointe", "Airport"], id: \.self) {
                            Text($0)
                        }
                    }
                    .pickerStyle(MenuPickerStyle())
                }

                VStack {
                    Text("Drop-Off Location:")
                    Picker("Drop-Off", selection: $selectedDropoffLocation) {
                        ForEach(["Scott Campus", "Dodge Campus", "Aksarben Village", "Village Pointe", "Airport"], id: \.self) {
                            Text($0)
                        }
                    }
                    .pickerStyle(MenuPickerStyle())
                }
            }
            .padding()
            .navigationTitle("Ride Sharing App")
        }
    }
}

struct RideSharingButton: View {
    var title: String

    var body: some View {
        Text(title)
            .padding()
            .background(Color.blue)
            .foregroundColor(.white)
            .cornerRadius(8)
    }
}

struct ContentView_Previews: PreviewProvider {
    static var previews: some View {
        ContentView()
    }
}

struct ProfileView: View {
    var body: some View {
        Text("Profile Screen")
    }
}

struct ViewRidesView: View {
    var body: some View {
        Text("View Rides Screen")
    }
}

struct ManageRidesView: View {
    var body: some View {
        Text("Manage Rides Screen")
    }
}
