from wagtail.models import Page

from wagtail.fields import RichTextField
from wagtail.admin.panels import FieldPanel
from wagtail.contrib.routable_page.models import RoutablePageMixin, path, route

from django.utils import timezone
from tournament.models import Tournament

from home.views import index, result


class LandingPage(RoutablePageMixin, Page):
    is_creatable = False

    heading = RichTextField(
        null=False,
        blank=False,
        default="Tenetur nesciunt quae aspernatur, incidunt suscipit beatae totam qui ut, nam possimus adipisci cum quaerat? Odio maxime sint, officiis excepturi veritatis quod accusantium quidem corporis sapiente delectus ut, ullam cum a praesentium ea nam soluta molestiae, blanditiis assumenda quia beatae. In veritatis quod nisi incidunt suscipit nesciunt iure. Rerum deserunt ad ipsum repudiandae magni exercitationem laboriosam amet saepe labore illo? Maxime modi temporibus suscipit impedit, libero alias nostrum ipsa consequuntur dignissimos, eveniet alias qui aperiam ex ipsam ipsa quod ea. Similique eligendi est delectus ipsa ullam quisquam quis inventore voluptas corrupti, mollitia dolorum ab veniam voluptatibus ex alias debitis ratione. Quae fugit expedita, veniam id tenetur veritatis, voluptatum corrupti nam ipsam sed quidem quam iste modi soluta, omnis magnam similique corporis voluptates rerum quidem est sed? Corporis distinctio non sunt alias, necessitatibus inventore asperiores, ea dolore dolor autem, atque sunt eius soluta minima nostrum aspernatur facere doloremque? In dolores fugit nihil iusto officia, fugit atque impedit porro totam magnam, qui ea repudiandae corporis repellat aspernatur, et dolorem voluptatem explicabo eligendi quibusdam? Et odio harum sed non voluptatum suscipit asperiores, facilis voluptate dolore nihil aliquam ab qui non dolor quisquam? Quam a provident, non vitae facere dolorem recusandae, id quis beatae cum sapiente, voluptate vero corporis soluta culpa recusandae officiis delectus, maiores beatae excepturi quam hic accusantium. Voluptatem ex quisquam inventore dolor ea minus libero nam, distinctio hic deleniti reiciendis nobis accusamus magnam atque, earum doloribus culpa ullam eveniet quae qui aliquam sapiente nisi explicabo, ratione eius aperiam pariatur sit maxime hic laudantium, quisquam animi deserunt in itaque harum veniam velit culpa provident dolor veritatis. Placeat ullam nesciunt expedita atque? Ab recusandae animi illum beatae nihil perferendis qui id provident, facere tempora similique.",
    )

    content_panels = Page.content_panels + [
        FieldPanel("heading"),
    ]

    @route(r"^$")
    def index(self, request):
        return index(request)

    @path("result/")
    def result(self, request):
        return result(request)

    @property
    def actual_tournament(self):
        active_tournament = Tournament.active_tournament()
        if not active_tournament:
            return None
        return active_tournament

    @property
    def last_result(self):
        last_tournament = (
            Tournament.objects.filter(end_date__lte=timezone.localtime())
            .order_by("-end_date")
            .first()
        )
        return last_tournament.get_results if last_tournament else None
