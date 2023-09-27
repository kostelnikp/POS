public class App {
    public static void main(String[] args) {
        MessageReader mr = new MessageReader();
        MessageSender ms = new MessageSender();

        mr.start();
        ms.start();
    }
}
